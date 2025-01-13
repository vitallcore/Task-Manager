from django.db import models
from django.contrib.auth import get_user_model
from task_manager.statuses.models import Status
from task_manager.labels.models import Label


class Task(models.Model):
    name = models.CharField(max_length=150, unique=True, null=False)

    description = models.TextField(blank=True)

    status = models.ForeignKey(Status, on_delete=models.PROTECT, null=False)

    executor = models.ForeignKey(
        get_user_model(), on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="executor"
    )

    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        null=False,
        related_name="author"
    )

    labels = models.ManyToManyField(
        Label,
        through="TasksWithLabels",
        related_name="labels"
    )
    created_at = models.DateTimeField(auto_now_add=True)


class TasksWithLabels(models.Model):
    label = models.ForeignKey(Label, on_delete=models.PROTECT)
    task = models.ForeignKey(Task, null=True, on_delete=models.SET_NULL)
