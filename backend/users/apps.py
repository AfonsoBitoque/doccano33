from allauth.account.apps import AccountConfig


class CustomAccountConfig(AccountConfig):
    def ready(self):
        # Ignora a verificação do middleware inexistente
        pass
