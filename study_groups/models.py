from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Course(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.code} - {self.name}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_study_times = models.TextField()  # Example: "Evenings, Weekends"
    learning_style = models.CharField(max_length=50)  # Example: "Visual Learner"
    strengths = models.TextField()  # Example: "Good at Calculus, Physics"
    location = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.username


class UserCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    schedule = models.TextField()  # Example: "MWF 10:00-11:00 AM"

    def __str__(self):
        return f"{self.user.username} - {self.course.name}"


class StudyGroup(models.Model):
    name = models.CharField(max_length=255)
    schedule = models.TextField(default='No schedule provided')
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    description = models.TextField(default='No description provided.')
    members = models.ManyToManyField(
        User,
        through="Membership",
        related_name="study_groups",
    )

    def __str__(self):
        return self.name

    def member_count(self):
        return self.members.count()


class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    study_group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "study_group")

    def __str__(self):
        return f"{self.user.username} -> {self.study_group.name}"


class StudySessionRating(models.Model):
    study_group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} rated {self.study_group.name} {self.rating}/5"


class Message(models.Model):
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, related_name="messages")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content[:30]}"


class SharedFile(models.Model):
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, related_name="shared_files")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to="shared_files/")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} shared {self.file.name}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.message}"
