from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Board(models.Model):
    title = models.CharField(max_length=64)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="boards_created"
    )
    members = models.ManyToManyField(User, related_name="boards")


class Task(models.Model):
    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"

    class Status(models.TextChoices):
        TO_DO = "to-do", "To do"
        IN_PROGRESS = "in-progress", "In progress"
        REVIEW = "review", "Review"
        DONE = "done", "Done"

    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=10, choices=Priority.choices)
    status = models.CharField(max_length=20, choices=Status.choices)
    due_date = models.DateField(null=True, blank=True)
    assignee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tasks_assigned",
    )
    reviewer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tasks_reviewing",
    )


class TaskComment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments_created"
    )
    content = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
