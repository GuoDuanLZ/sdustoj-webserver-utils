from .mixins import ExtendCreateModelMixin, ExtendUpdateModelMixin
from .mixins import UserCreateModelMixin, UserUpdateModelMixin
from rest_framework import viewsets, mixins, filters

from django.shortcuts import get_object_or_404


class FilterViewSet(viewsets.GenericViewSet):
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)


class ModelFilterViewSet(mixins.ListModelMixin, ExtendCreateModelMixin,
                         mixins.RetrieveModelMixin, ExtendUpdateModelMixin, mixins.DestroyModelMixin,
                         FilterViewSet):
    pass


resource_required_user_fields = [('creator', 'username', True), ('updater', 'username', False)]


class ResourceListViewSet(mixins.ListModelMixin, UserCreateModelMixin,
                          FilterViewSet):
    required_user_fields = resource_required_user_fields


class ResourceDetailViewSet(mixins.RetrieveModelMixin, UserUpdateModelMixin, mixins.DestroyModelMixin,
                            FilterViewSet):
    required_user_fields = resource_required_user_fields


class ResourceViewSet(mixins.ListModelMixin, UserCreateModelMixin,
                      mixins.RetrieveModelMixin, UserUpdateModelMixin, mixins.DestroyModelMixin,
                      FilterViewSet):
    required_user_fields = resource_required_user_fields


class NestedMixin(object):
    parent_queryset = None          # 父类的查询集
    parent_lookup = None            # 在视图类中传递的参数中代表父类的参数的名字
    parent_related_name = None      # 父类中表示子类的属性名
    parent_pk_field = None          # 父类的主键

    def get_parent(self, kwargs):
        if self.parent_lookup is not None:
            lookup_value = kwargs.get(self.parent_lookup)
            if lookup_value is not None:
                parent = get_object_or_404(self.parent_queryset, **{self.parent_pk_field: lookup_value})
                return parent
        return None

    def set_list_queryset(self, kwargs):
        parent = self.get_parent(kwargs)
        if parent is not None:
            self.queryset = self.queryset.filter(**{self.parent_related_name: parent})


class NestedListViewSet(mixins.ListModelMixin, ExtendCreateModelMixin, NestedMixin,
                        FilterViewSet):
    def list(self, request, *args, **kwargs):
        self.set_list_queryset(kwargs)
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        parent = self.get_parent(kwargs)
        extra_data = self.extra_data
        extra_data[self.parent_related_name] = parent
        return super().create(request, *args, **kwargs)


class NestedListOnlyViewSet(mixins.ListModelMixin, NestedMixin, FilterViewSet):
    def list(self, request, *args, **kwargs):
        self.set_list_queryset(kwargs)
        return super().list(request, *args, **kwargs)


class NestedCreateOnlyViewSet(ExtendCreateModelMixin, NestedMixin, FilterViewSet):
    def create(self, request, *args, **kwargs):
        parent = self.get_parent(kwargs)
        extra_data = self.extra_data
        extra_data[self.parent_related_name] = parent
        return super().create(request, *args, **kwargs)


class NestedDetailViewSet(mixins.RetrieveModelMixin, UserUpdateModelMixin, NestedMixin,
                          FilterViewSet):
    pass


class NestedReadOnlyViewSet(mixins.ListModelMixin, NestedMixin, mixins.RetrieveModelMixin,
                            FilterViewSet):
    def list(self, request, *args, **kwargs):
        self.set_list_queryset(kwargs)
        return super().list(request, *args, **kwargs)


class NestedResourceListViewSet(mixins.ListModelMixin, UserCreateModelMixin, NestedMixin, FilterViewSet):
    required_user_fields = resource_required_user_fields

    def list(self, request, *args, **kwargs):
        self.set_list_queryset(kwargs)
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        parent = self.get_parent(kwargs)
        extra_data = self.extra_data
        extra_data[self.parent_related_name] = parent
        return super().create(request, *args, **kwargs)


class NestedResourceListOnlyViewSet(mixins.ListModelMixin, NestedMixin, FilterViewSet):
    required_user_fields = resource_required_user_fields

    def list(self, request, *args, **kwargs):
        self.set_list_queryset(kwargs)
        return super().list(request, *args, **kwargs)


class NestedResourceCreateOnlyViewSet(UserCreateModelMixin, NestedMixin, FilterViewSet):
    required_user_fields = resource_required_user_fields

    def create(self, request, *args, **kwargs):
        parent = self.get_parent(kwargs)
        extra_data = self.extra_data
        extra_data[self.parent_related_name] = parent
        return super().create(request, *args, **kwargs)


class NestedResourceDetailViewSet(mixins.RetrieveModelMixin, UserUpdateModelMixin, mixins.DestroyModelMixin,
                                  NestedMixin,
                                  FilterViewSet):
    required_user_fields = resource_required_user_fields


class NestedResourceReadOnlyViewSet(NestedReadOnlyViewSet):
    pass