from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .celery_tasks import check_uploaded_files, upload_to_store
from .datasets import load_dataset
from .pipeline.catalog import Options, create_file_format
from .pipeline.exceptions import FileImportException
from .pipeline.readers import FileName
from django.conf import settings
from django.contrib.auth import get_user_model
from django_drf_filepond.models import TemporaryUpload
from projects.models import Project
from projects.permissions import IsProjectAdmin


class DatasetCatalog(APIView):
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    def get(self, request, *args, **kwargs):
        project_id = kwargs["project_id"]
        project = get_object_or_404(Project, pk=project_id)
        use_relation = getattr(project, "use_relation", False)
        options = Options.filter_by_task(project.project_type, use_relation)
        return Response(data=options, status=status.HTTP_200_OK)


class DatasetImportAPI(APIView):
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    def post(self, request, *args, **kwargs):
        upload_ids = request.data.pop("uploadIds")
        file_format = request.data.pop("format")
        task = request.data.pop("task")
        project_id = self.kwargs["project_id"]
        user_id = request.user.id
        
        # Processamento síncrono direto
        try:
            project = get_object_or_404(Project, pk=project_id)
            user = get_object_or_404(get_user_model(), pk=user_id)
            fmt = create_file_format(file_format)
            upload_ids, errors = check_uploaded_files(upload_ids, fmt)
            
            if not upload_ids:
                return Response({"error": [e.dict() for e in errors] + ["No valid files to import."]}, status=status.HTTP_400_BAD_REQUEST)

            temporary_uploads = TemporaryUpload.objects.filter(upload_id__in=upload_ids)
            filenames = [
                FileName(full_path=tu.get_file_path(), generated_name=tu.file.name, upload_name=tu.upload_name)
                for tu in temporary_uploads
            ]

            dataset = load_dataset(task, fmt, filenames, project, **request.data)
            dataset.save(user, batch_size=settings.IMPORT_BATCH_SIZE)
            upload_to_store(temporary_uploads)
            errors.extend(dataset.errors)
            
            return Response({"result": {"error": [e.dict() for e in errors]}}, status=status.HTTP_200_OK)
        except FileImportException as e:
            return Response({"error": [e.dict()]}, status=status.HTTP_400_BAD_REQUEST)
