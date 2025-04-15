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

from rest_framework import generics, status
from rest_framework.response import Response
from .models import UserAnswer

# Custom permission class to allow any user
from rest_framework.permissions import AllowAny
class SubmitAnswersView(generics.CreateAPIView):
    permission_classes = [AllowAny]  # Allow any user to access this view

    def post(self, request, challenge_id):
        answers = request.data.get('answers', [])
        print(answers)
        user = request.user
        certificate_generated = False  # Flag to check if certificate is generated

        for answer in answers:
            question_id = answer.get('questionId')
            user_answer = answer.get('answer')

            # Check if the user is authenticated
            if user.is_authenticated:
                # Get the question to check the correct flag
                question = Question.objects.get(id=question_id)
                is_correct = user_answer == question.flag  # Check if the answer matches the flag

                # Save the user's answer
                UserAnswer.objects.update_or_create(
                    user=user,
                    question=question,
                    defaults={'answer': user_answer, 'is_correct': is_correct}
                )

                # If the answer is correct, generate the certificate
                if is_correct and not certificate_generated:
                    self.generate_certificate(user, challenge_id)
                    certificate_generated = True  # Ensure we only generate one certificate

            else:
                # Handle unauthenticated user case
                UserAnswer.objects.update_or_create(
                    user=None,  # Or handle as needed
                    question_id=question_id,
                    defaults={'answer': user_answer, 'is_correct': user_answer == question.flag}
                )

        return Response({'message': 'Answers submitted successfully!'}, status=status.HTTP_201_CREATED)

    def generate_certificate(self, user, challenge_id):
        # Create a certificate image
        certificate = Image.new('RGB', (800, 600), color='white')
        draw = ImageDraw.Draw(certificate)

        # Load a font
        font = ImageFont.load_default()

        # Draw text on the certificate
        draw.text((100, 100), "Certificate of Completion", fill="black", font=font)
        draw.text((100, 200), f"This certifies that {user.username}", fill="black", font=font)
        draw.text((100, 300), "has successfully completed the challenge.", fill="black", font=font)

        # Save the certificate to a BytesIO object
        buffer = BytesIO()
        certificate.save(buffer, format='PNG')
        buffer.seek(0)

        # Save the certificate to the default storage
        file_name = f"certificates/{user.username}_certificate.png"
        default_storage.save(file_name, ContentFile(buffer.getvalue()))

        # Optionally, you can return the URL of the generated certificate
        return f"http://localhost:8000/media/{file_name}"
    
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
    

from rest_framework import generics, status
from rest_framework.response import Response
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from .models import UserAnswer

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile  # Assuming you have a UserProfile model to store user data

class GenerateCertificateView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # Fetch certificates for the user
        certificates = []  # Replace with actual logic to fetch certificates

        # Assuming you have a way to get the certificates from the UserProfile or UserAnswer
        user_answers = UserAnswer.objects.filter(user=user)
        for answer in user_answers:
            # Assuming you have a way to get the challenge name and certificate URL
            challenge_name = answer.question.challenge.name  # Adjust according to your model
            certificate_url = f"http://localhost:8000/media/certificates/{user.username}_certificate.png"  # Adjust path as needed
            certificates.append({
                'id': answer.id,
                'challenge_name': challenge_name,
                'url': certificate_url,
            })

        return Response(certificates, status=status.HTTP_200_OK)

