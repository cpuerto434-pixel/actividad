from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks"
    )

    def __str__(self):
        return self.title
