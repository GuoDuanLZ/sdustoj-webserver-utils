from rest_framework.mixins import CreateModelMixin, UpdateModelMixin


class ExtraDataMixin(object):
    def __init__(self, *args, **kwargs):
        self.extra_data = dict()
        super().__init__(*args, **kwargs)


class ExtendCreateModelMixin(CreateModelMixin, ExtraDataMixin):
    def perform_create(self, serializer):
        instance = serializer.save(**self.extra_data)
        return instance


class ExtendUpdateModelMixin(UpdateModelMixin, ExtraDataMixin):
    def perform_update(self, serializer):
        instance = serializer.save(**self.extra_data)
        return instance


class UserMixin(object):
    """
    提供方法使视图类在创建或更新时可以同时设置用户的信息。
    需要设置required_user_fields:
    格式为：
        [
            (需要设置的field, 设置为用户的哪个field的值),
            ......
        ]
    """
    required_user_fields = []

    def _set_user_fields(self, request, is_create=False):
        user = request.user
        if user is not None:
            for (to_set_field, user_field, only_create) in self.required_user_fields:
                if is_create or (not only_create):
                    if user_field is None:
                        value = user
                    else:
                        value = getattr(user, user_field)

                    self.extra_data[to_set_field] = value


class UserCreateModelMixin(ExtendCreateModelMixin, UserMixin):
    def create(self, request, *args, **kwargs):
        self._set_user_fields(request, is_create=True)
        return super().create(request, *args, **kwargs)


class UserUpdateModelMixin(ExtendUpdateModelMixin, UserMixin):
    def update(self, request, *args, **kwargs):
        self._set_user_fields(request, is_create=False)
        return super().update(request, *args, **kwargs)
