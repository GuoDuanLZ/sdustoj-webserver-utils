from rest_framework import filters
import django_filters


class ResourceFilter(filters.FilterSet):
    create_time_gte = django_filters.DateTimeFilter(name='create_time', lookup_expr='gte')
    create_time_lte = django_filters.DateTimeFilter(name='create_time', lookup_expr='lte')
    update_time_gte = django_filters.DateTimeFilter(name='update_time', lookup_expr='gte')
    update_time_lte = django_filters.DateTimeFilter(name='update_time', lookup_expr='lte')
    creator = django_filters.CharFilter(name='creator')
    updater = django_filters.CharFilter(name='updator')

    resource_fields = ('create_time', 'update_time', 'creator', 'updater')


resource_ordering = ('create_time', 'update_time', 'creator', 'updater')
