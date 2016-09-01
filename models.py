from django.db import models


class ModifyInfo(models.Model):
    read_only = ('creator', 'create_time', 'updater', 'update_time',)

    creator = models.CharField(max_length=30)
    create_time = models.DateTimeField(auto_now_add=True)
    updater = models.CharField(max_length=30)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Resource(ModifyInfo):
    title = models.CharField(max_length=128)
    introduction = models.CharField(max_length=512, null=True)

    class Meta:
        abstract = True


class SourceMixin(models.Model):
    source = models.CharField(max_length=256, null=True)
    author = models.CharField(max_length=32, null=True)

    class Meta:
        abstract = True


class StatusMixin(models.Model):
    STATUS_CHOICES = (
        (1, 'available'),
        (0, 'unavailable'),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)

    class Meta:
        abstract = True
