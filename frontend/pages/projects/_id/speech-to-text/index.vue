<template>
  <layout-text v-if="example.id">
    <template #header>
      <toolbar-laptop
        :doc-id="example.id"
        :enable-auto-labeling.sync="enableAutoLabeling"
        :guideline-text="project.guideline"
        :is-reviewd="example.isConfirmed"
        :total="totalExample"
        class="d-none d-sm-block"
        @click:clear-label="clear(example.id)"
        @click:review="confirm(projectId)"
      />
      <toolbar-mobile :total="totalExample" class="d-flex d-sm-none" />
    </template>
    <template #content>
      <v-overlay :value="isLoading">
        <v-progress-circular indeterminate size="64" />
      </v-overlay>
      <audio-viewer :source="example.url" class="mb-5" />
      <seq2seq-box
        :text="example.text"
        :annotations="labels"
        @delete:annotation="(labelId) => remove(example.id, labelId)"
        @update:annotation="(labelId, text) => update(example.id, labelId, text)"
        @create:annotation="(text) => add(example.id, text)"
      />
    </template>
    <template #sidebar>
      <annotation-progress :progress="progress" />
      <list-metadata :metadata="example.meta" class="mt-4" />
    </template>
  </layout-text>
</template>

<script>
import { ref, toRefs, useContext, useFetch, watch } from '@nuxtjs/composition-api'
import LayoutText from '@/components/tasks/layout/LayoutText'
import ListMetadata from '@/components/tasks/metadata/ListMetadata'
import AnnotationProgress from '@/components/tasks/sidebar/AnnotationProgress.vue'
import ToolbarLaptop from '@/components/tasks/toolbar/ToolbarLaptop'
import ToolbarMobile from '@/components/tasks/toolbar/ToolbarMobile'
import AudioViewer from '~/components/tasks/audio/AudioViewer'
import Seq2seqBox from '~/components/tasks/seq2seq/Seq2seqBox'
import { useExampleItem } from '~/composables/useExampleItem'
import { useProjectItem } from '~/composables/useProjectItem'
import { useTextLabel } from '~/composables/useTextLabel'

export default {
  components: {
    AnnotationProgress,
    AudioViewer,
    LayoutText,
    ListMetadata,
    Seq2seqBox,
    ToolbarLaptop,
    ToolbarMobile
  },
  layout: 'workspace',

  validate({ params, query }) {
    return /^\d+$/.test(params.id) && /^\d+$/.test(query.page)
  },

  setup() {
    const { app, params, query } = useContext()
    const projectId = params.value.id
    const { state: projectState, getProjectById } = useProjectItem()
    const {
      state: labelState,
      autoLabel,
      list,
      clear,
      remove,
      add,
      update
    } = useTextLabel(app.$repositories.textLabel, projectId)
    const { state: exampleState, confirm, getExample, updateProgress } = useExampleItem()
    const enableAutoLabeling = ref(false)
    const isLoading = ref(false)

    getProjectById(projectId)
    updateProgress(projectId)

    const { fetch } = useFetch(async () => {
      isLoading.value = true
      await getExample(projectId, query.value)
      if (enableAutoLabeling.value && exampleState.example && exampleState.example.id) {
        try {
          await autoLabel(projectId, exampleState.example.id)
        } catch (e) {
          enableAutoLabeling.value = false
        }
      } else if (exampleState.example && exampleState.example.id) {
        await list(exampleState.example.id)
      }
      isLoading.value = false
    })
    watch(query, fetch)
    watch(enableAutoLabeling, async (val) => {
      if (val && 
          exampleState.example && 
          exampleState.example.id && 
          !exampleState.example.isConfirmed) {
        await autoLabel(projectId, exampleState.example.id)
        await getTeacherList(projectId, exampleState.example.id)
      }
    })

    return {
      ...toRefs(labelState),
      ...toRefs(exampleState),
      ...toRefs(projectState),
      add,
      list,
      clear,
      remove,
      update,
      confirm,
      enableAutoLabeling,
      projectId,
      isLoading
    }
  }
}
</script>
