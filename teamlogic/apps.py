from django.apps import AppConfig

class TeamLogicConfig(AppConfig):
    name = 'teamlogic'
    verbose_name = 'Team Logic'

    def ready(self):
        import signals
