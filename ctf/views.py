# ctf_app/views.py
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from .models import Challenge, UserProfile, Participation,StudentDetail
from .serializers import ChallengeSerializer, UserProfileSerializer, ParticipationSerializer,StudentDetailSerializer
from django.db.models import Count
from rest_framework.permissions import IsAuthenticated
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
        
class StudentDetailView(generics.CreateAPIView):
    serializer_class = StudentDetailSerializer
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        print("Received request to save student details.")
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            print("Serializer is valid. Processing data...")
            student_detail, created = StudentDetail.objects.get_or_create(user=request.user)
            student_detail.college = serializer.validated_data['college']
            student_detail.roll_number = serializer.validated_data['roll_number']
            student_detail.save()
            print(f"Student details saved: {student_detail}")
            return Response({'message': 'Student details saved successfully!'}, status=status.HTTP_201_CREATED)

        print("Serializer errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LeaderboardView(generics.ListAPIView):
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        queryset = UserProfile.objects.all().order_by('-points', '-challenges_solved')
        print(f"Leaderboard data: {queryset}")  # Print the queryset
        return queryset

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
from rest_framework.permissions import IsAuthenticated
class JoinChallengeView(generics.GenericAPIView):
    # permission_classes = [IsAuthenticated]
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
        

from rest_framework import generics, status
from rest_framework.response import Response
from .models import UserAnswer, Question, UserProfile

class CheckAnswerView(generics.GenericAPIView):
    def post(self, request, question_id):
        try:
            question = Question.objects.get(id=question_id)
            user_answer = request.data.get('answer')

            # Create or update the user's answer
            user_answer_instance, created = UserAnswer.objects.get_or_create(
                user=request.user,
                question=question,
                defaults={'answer': user_answer}
            )

            # Check if the answer is correct
            if user_answer == question.flag:
                user_answer_instance.is_correct = True
                user_answer_instance.save()

                # Update or create the user's profile
                user_profile, created = UserProfile.objects.get_or_create(user=request.user)
                user_profile.points += question.points
                user_profile.challenges_solved += 1  # Increment challenges solved
                user_profile.save()

                return Response({'message': 'Correct answer! Points awarded.'}, status=status.HTTP_200_OK)
            else:
                user_answer_instance.is_correct = False
                user_answer_instance.save()
                return Response({'message': 'Incorrect answer.'}, status=status.HTTP_400_BAD_REQUEST)

        except Question.DoesNotExist:
            return Response({'error': 'Question not found.'}, status=status.HTTP_404_NOT_FOUND)
        

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Challenge, Question, UserAnswer
from .serializers import QuestionSerializer

class ChallengeQuestionsView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, challenge_id):
        try:
            challenge = Challenge.objects.get(id=challenge_id)
            questions = Question.objects.filter(challenge=challenge)
            serializer = QuestionSerializer(questions, many=True)
            return Response({'challenge': challenge.name, 'questions': serializer.data}, status=status.HTTP_200_OK)
        except Challenge.DoesNotExist:
            return Response({'error': 'Challenge not found.'}, status=status.HTTP_404_NOT_FOUND)

class SubmitAnswersView(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, challenge_id):
        answers = request.data.get('answers', [])
        for answer in answers:
            question_id = answer.get('questionId')
            user_answer = answer.get('answer')

            # Save the user's answer
            UserAnswer.objects.update_or_create(
                user=request.user,
                question_id=question_id,
                defaults={'answer': user_answer}
            )

        return Response({'message': 'Answers submitted successfully!'}, status=status.HTTP_201_CREATED)
    
class UserStatsView(generics.RetrieveAPIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            data = {
                'username': user_profile.user.username,
                'points': user_profile.points,
                'challenges_solved': user_profile.challenges_solved,
            }
            return Response(data, status=200)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User profile not found.'}, status=404)
    

