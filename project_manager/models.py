from django.db import models
from django.contrib.auth.models import User


ON_HOLD = "OH"
NOT_STARTED = "NS"
IN_PROGRESS = "IP"
COMPLETED = "C"
STATUS_CHOICES = [
    (ON_HOLD, "ON HOLD"),
    (NOT_STARTED, "NOT STARTED"),
    (IN_PROGRESS, "IN PROGRESS"),
    (COMPLETED, "COMPLETE"),
]

LOW = "L"
HIGH = "H"
PRIORITY_CHOICES = [
    (LOW, "LOW"),
    (HIGH, "HIGH"),
]


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="member")
    organization = models.ForeignKey(
        "Organization",
        on_delete=models.CASCADE,
        related_name="members",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.user.username


class Project(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    deadline = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default=LOW)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default=NOT_STARTED
    )
    members = models.ManyToManyField(
        "Member", related_name="project_members", blank=True
    )
    author = models.ForeignKey(
        "Member", on_delete=models.CASCADE, related_name="project_authored"
    )
    organization = models.ForeignKey(
        "Organization",
        on_delete=models.CASCADE,
        related_name="projects",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title

    def completion(self):
        try:
            return round(
                self.project_milestones.filter(status=COMPLETED).count()
                / self.project_milestones.all().count()
                * 100
            )
        except ZeroDivisionError:
            return 0


class Milestone(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    deadline = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default=NOT_STARTED
    )
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default=LOW)
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, related_name="project_milestones"
    )
    assignment = models.ForeignKey(
        "Member",
        on_delete=models.CASCADE,
        related_name="milestones_assignments",
        blank=True,
        null=True,
    )
    author = models.ForeignKey(
        "Member", on_delete=models.CASCADE, related_name="milestones_authored"
    )

    def __str__(self):
        return f"{self.priority} - {self.title}"

    def completion(self):
        try:
            return round(
                self.milestone_tasks.filter(status=COMPLETED).count()
                / self.milestone_tasks.all().count()
                * 100
            )
        except ZeroDivisionError:
            return 0

    class Meta:
        ordering = ["deadline"]


class Task(models.Model):
    title = models.CharField(max_length=64)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default=NOT_STARTED
    )
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default=LOW)

    class Meta:
        abstract = True


class MilestoneTask(models.Model):
    title = models.CharField(max_length=64)
    milestone = models.ForeignKey(
        "Milestone", on_delete=models.CASCADE, related_name="tasks"
    )
    complete = models.BooleanField(default=False)


class DayTask(Task):
    user = models.ForeignKey(
        "Member", on_delete=models.CASCADE, related_name="day_tasks"
    )
    parent = models.ForeignKey(
        "DayTask",
        on_delete=models.CASCADE,
        related_name="childs",
        null=True,
        blank=True,
    )


class Organization(models.Model):
    title = models.CharField(max_length=64)
    login = models.CharField(max_length=64, null=True)
    password = models.CharField(max_length=32, null=True)

    def __str__(self):
        return self.title
