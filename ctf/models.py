from django.db import models
from back.models import User

from django.db import models
from django.utils import timezone

class Challenge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    active = models.BooleanField(default=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['-created_at']

class Question(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=200)
    description = models.TextField()
    flag = models.CharField(max_length=100, help_text="The correct flag/answer for this question.")
    points = models.IntegerField(default=100, help_text="Points awarded for solving this question.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} (in {self.challenge.name})"

    class Meta:
        ordering = ['created_at']

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    points = models.IntegerField(default=0)
    challenges_solved = models.IntegerField(default=0)  # Add this field

    def __str__(self):
        return f"{self.user.username} - {self.points} points"

class Participation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participations')
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='participants')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'challenge')

    def __str__(self):
        return f"{self.user.username} in {self.challenge.name}"
    
class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='user_answers')
    answer = models.CharField(max_length=100)  # User's submitted answer
    is_correct = models.BooleanField(default=False)  # To track if the answer is correct
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.question.title} - {'Correct' if self.is_correct else 'Incorrect'}"
    
class StudentDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_detail')
    college = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username} - {self.college}"