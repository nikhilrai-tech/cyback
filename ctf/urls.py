# ctf_app/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChallengeViewSet,StudentDetailView, LeaderboardView, ParticipationStatsView, JoinChallengeView,CheckAnswerView,ChallengeQuestionsView,SubmitAnswersView,UserStatsView

router = DefaultRouter()
router.register(r'challenges', ChallengeViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
    path('api/stats/', ParticipationStatsView.as_view(), name='participation-stats'),
    path('api/challenge/<int:challenge_id>/join/', JoinChallengeView.as_view(), name='join-challenge'),
    path('api/check-answer/<int:question_id>/', CheckAnswerView.as_view(), name='check-answer'),
    path('api/challenges/<int:challenge_id>/questions/', ChallengeQuestionsView.as_view(), name='challenge-questions'),
    path('api/challenges/<int:challenge_id>/submit-answers/', SubmitAnswersView.as_view(), name='submit-answers'),
    path('api/leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
    path('api/user/stats/', UserStatsView.as_view(), name='user-stats'),
    path('api/student/details/', StudentDetailView.as_view(), name='student-details'),
]