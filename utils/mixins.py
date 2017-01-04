from django.conf import settings


class PaginatedViewMixin(object):
    paginate_by = getattr(settings, 'PAGINATE_BY', 10)
