from django.apps import AppConfig


class DomainUserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'domain.user'
    # Django: abstract-user
    label = 'domain_user'