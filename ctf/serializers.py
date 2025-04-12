# ctf_app/serializers.py
from rest_framework import serializers
from .models import Challenge, UserProfile, Participation
from django.contrib.auth.models import User

class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = ['id', 'name', 'description', 'active', 'start_date', 'end_date']

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['username', 'points']

class ParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participation
        fields = ['user', 'challenge', 'joined_at']