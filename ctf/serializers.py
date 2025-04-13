# ctf_app/serializers.py
from rest_framework import serializers
from .models import Challenge, UserProfile, Participation,Question,StudentDetail
from django.contrib.auth.models import User

class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = ['id', 'name', 'description', 'active', 'start_date', 'end_date']

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['username', 'points', 'challenges_solved']  # Include challenges_solved

class ParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participation
        fields = ['user', 'challenge', 'joined_at']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'title', 'description', 'points']  # Include points if needed

class SubmitAnswerSerializer(serializers.Serializer):
    questionId = serializers.IntegerField()

class StudentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentDetail
        fields = ['college', 'roll_number']