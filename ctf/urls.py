# ctf_app/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChallengeViewSet, LeaderboardView, ParticipationStatsView, JoinChallengeView

router = DefaultRouter()
router.register(r'challenges', ChallengeViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
    path('api/stats/', ParticipationStatsView.as_view(), name='participation-stats'),
    path('api/challenge/<int:challenge_id>/join/', JoinChallengeView.as_view(), name='join-challenge'),
]