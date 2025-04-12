# ctf_app/views.py
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from .models import Challenge, UserProfile, Participation
from .serializers import ChallengeSerializer, UserProfileSerializer, ParticipationSerializer
from django.db.models import Count

from rest_framework import viewsets
from .models import Challenge
from .serializers import ChallengeSerializer
from django.utils import timezone

class ChallengeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer

    def get_queryset(self):
        print("Fetching challenges...")
        now = timezone.now()
        print(f"Current time: {now}")

        try:
            challenges = Challenge.objects.filter(end_date__gte=now)
            print(f"Found {challenges.count()} active challenges.")
            return challenges
        except Exception as e:
            print(f"Error fetching challenges: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LeaderboardView(generics.ListAPIView):
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        print("Fetching leaderboard...")
        try:
            queryset = UserProfile.objects.all().order_by('-points')
            print(f"Found {queryset.count()} users in the leaderboard.")
            return queryset
        except Exception as e:
            print(f"Error fetching leaderboard: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ParticipationStatsView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        # Get participation count per challenge
        participation_data = Participation.objects.values('challenge__name').annotate(count=Count('user'))
        # Get active/inactive challenge counts
        active_count = Challenge.objects.filter(active=True).count()
        inactive_count = Challenge.objects.filter(active=False).count()

        return Response({
            'participation': [
                {'challenge': item['challenge__name'], 'users': item['count']}
                for item in participation_data
            ],
            'challenge_status': {
                'active': active_count,
                'inactive': inactive_count
            }
        })

class JoinChallengeView(generics.GenericAPIView):
    def post(self, request, challenge_id, *args, **kwargs):
        print(f"User {request.user.username} is trying to join challenge {challenge_id}...")
        try:
            challenge = Challenge.objects.get(id=challenge_id, active=True)
            participation, created = Participation.objects.get_or_create(
                user=request.user,
                challenge=challenge
            )
            if created:
                print(f"User {request.user.username} successfully joined challenge {challenge.name}.")
                return Response({'message': 'Successfully joined the challenge'}, status=status.HTTP_201_CREATED)
            print(f"User {request.user.username} is already participating in challenge {challenge.name}.")
            return Response({'message': 'Already participating in this challenge'}, status=status.HTTP_200_OK)
        except Challenge.DoesNotExist:
            print(f"Challenge {challenge_id} not found or not active.")
            return Response({'error': 'Challenge not found or not active'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Error joining challenge: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)