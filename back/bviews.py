from django.db.models.query_utils import Q
from django.shortcuts import redirect, render
from .models import *
from rest_framework.authtoken.models import Token
from string import printable
# Create your views here.
from django.contrib.auth.tokens import default_token_generator
from datetime import datetime
# import mysqlclient
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes, authentication_classes 
from django.contrib.admin.models import LogEntry
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .serializers import *
from django import forms
# from PIL import Image
from other.notis import add_noti_single_email, add_noti_multiple_email
# from django.contrib.auth.tokens.default_token_generator import make_token
import re
from .email import send_html_mail

# accounts/views.py
from django.contrib.auth import get_user_model
from django.views.generic.detail import DetailView

from rest_framework.permissions import BasePermission
from main.serializers import ProgramSerializerShort
from main.models import Program

from back import email

User = get_user_model()


# Custom permission for users with "is_active" = True.
class IsCompany(BasePermission):
    def has_permission(self, request, view):
        try:
            user = User.objects.get(id=request.user.id)
            return user and user.is_company
        except:
            return False

class IsUser(BasePermission):
    def has_permission(self, request, view):
        try:
            user = User.objects.get(id=request.user.id)
            return user and not user.is_staff
        except:
            return False



# DOMAIN = 'http://localhost:3005'
DOMAIN = 'https://cyfront.vercel.app'
# Create your views here.
def index(request):
    # print(default_token_generator.check_token(User.objects.get(id=807),'auxmp2-985e1dd25fda9f30f4039cf11ace0a6b'))
    # return HttpResponse('This is a hacker organization app. Staying in this site for some time would cause several attacks to your device')
    # user = User.objects.get(id=97)
    # user.email_confirmed = True
    # user.save()
    # programs = Program.objects.all().delete()
    return render(request, 'index.html')






class CurrentLoggedInUser(ModelViewSet):
    queryset = get_user_model().objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer
    
    def retrieve(self, request, *args, **kwargs):
        # print(request.user)
        user_profile = self.queryset.get(email=request.user.email)
        serializer = self.get_serializer(user_profile)
        return Response({'user': serializer.data})


@api_view(['POST'])
def login(request): 
    # print(request.data)
    try:
        usern = User.objects.get(Q(username__iexact=request.data['username'])|Q(email=request.data['username']))
    except:
        return Response ({ "error": True,'message': 'Incorrect Username/Email or Password'})
    # user = authenticate(username=uname, password=request.data['password'])
    if usern.check_password(request.data['password']):
    # if user is not None:
        # auth.login(request, user)
        # print('done')
        # user=User.objects.get(id=request.user.id)
        if not usern.is_active and not usern.email_confirmed:
            tok = Token.objects.get_or_create(user=usern)
            token = default_token_generator.make_token(usern)
            send_html_mail('Activate Your Account ',{'link': DOMAIN + '/verify/?token=' + str(tok[0])+'&user='+ token,'name': usern.username,'code': token},'email/verify2.html',[usern.email],[],[],[])
            return Response ({ "error": True,'message': 'Account not active. We have sent an Email for Verification.'})
        if usern.type not in ['U','C','Ct']:
            return Response ({ "error": True,'message': 'Admins are not allowed to login here'})
        refresh = RefreshToken.for_user(usern)
        # print()
        return Response(
            {
                # "type": 'success',
                # "message": 'Authenticated',
                # "details": detailspack(user)
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'new_user': (datetime.now() - usern.date_joined).days < 90
            }
        )
    else:
        # user = User.objects.get(Q(username=request.data['username'])|Q(email=request.data['username']))
        # name = user.name if user.name else user.username
        send_html_mail('Failed Login Attempt',{'name': usern.name if usern.name else usern.username,'message': 'Dear '+usern.name if usern.name else usern.username+", We noticed a new sign in to your SecuriumX account. If it was you, you don't need to do anything. If not, please contact the admin"},'email/desc.html',[usern.email],[],[],[])
        return Response ({ "error": True,'message': 'Incorrect Username/Email or Password'})




@api_view(['POST'])
def signup(request): 
  #  print(request.data)
    if len(request.data['email']) < 1 or len(request.data['username']) < 1 or len(request.data['password']) < 1 or len(request.data['name']) < 1 or not re.match(r"[^@]+@[^@]+\.[^@]+", request.data['email']) or not re.match("^[a-zA-Z0-9_@ .-]+$", request.data['username']):
        return Response({"error": True,"message": 'Please Add Everything Properly'})
    # print()
    # print(re.match("/(<|%3C)script[\s\S]*?(>|%3E)[\s\S]*?(<|%3C)(\/|%2F)script[\s\S]*?(>|%3E)/gi", request.data['username']))
    # print(re.match(r'<(script).*?</\1>(?s)', request.data['username']))
    # return Response({"error": True,"message": "cjvnjcd"})
    try:
        user2 = User.objects.get(Q(username__iexact=request.data['username'])|Q(email=request.data['email']))
        # print(user2.email)
        return Response({"error": True,"message": 'User already exists with this Email/Username'})
    except:
        if 'refcode' in request.data:
            if len(request.data['refcode']) > 1:
                try:
                    refuser = User.objects.get(refcode=request.data['refcode'])
                    user = User.objects.create_user(username=request.data['username'],email=request.data['email'],password=request.data['password'],
                        name=request.data['name'] if 'name' in request.data else None,refuser=refuser,active=False)
                except Exception as err:
                    return Response({"error": True,"message": str(err)})
            else:
                user = User.objects.create_user(username=request.data['username'],email=request.data['email'],password=request.data['password'],
                    name=request.data['name'] if 'name' in request.data else None,active=False)
        else:
            user = User.objects.create_user(username=request.data['username'],email=request.data['email'],password=request.data['password'],
                name=request.data['name'] if 'name' in request.data else None,active=False)
        user.save()
        tok = Token.objects.create(user=user)
        try:
            token = default_token_generator.make_token(user)
            # print(token)
            send_html_mail('Activate Your Account ',{'link': DOMAIN + '/verify/?token=' + str(tok.key)+'&user='+ token,'name': user.name if user.name else user.username,'code': token},'email/verify2.html',[user.email],[],[],[])
            return Response(
                {   
                    "error": False,
                    "message": 'Authenticated',
                    # "cdsjfnbdsjfg" : str(tok.key)
                    # "details": detailspack(user),
                    # "code": code1
                }
            )
        except:
            return Response(
                {
                    "error": True,
                    "message": "Signup Successful but couldn't verify, Verify Later",
                    # "details": detailspack(user),
                    # "code": code1
                }
            )





@api_view(['POST'])
def companysignup(request): 
  #  print(request.data)
    if len(request.data['email']) < 1 or len(request.data['username']) < 1 or len(request.data['name']) < 1 or not re.match(r"[^@]+@[^@]+\.[^@]+", request.data['email']):
        return Response({"error": True,"message": 'Please Add Everything Properly'})
    # if :
    #     return Response({"error": True,"message": 'Enter a Valid Email'})
    try:
        user2 = User.objects.get(Q(username__iexact=request.data['username'])|Q(email=request.data['email']))
        return Response({"error": True,"message": 'Company already exists with this Email/Username'})
    except:
        user = User.objects.create_user(username=request.data['username'],email=request.data['email'],password=request.data['email'],
                name=request.data['name'] if 'name' in request.data else None,active=False,type='C')
        user.save()
        user.contact = request.data['contact']
        user.companytype = request.data['type']
        user.save()
        tok = Token.objects.create(user=user)
        try:
            token = default_token_generator.make_token(user)
            # print(token)
            send_html_mail('Activate Your Account ',{'link': DOMAIN + '/verify/?token=' + str(tok.key)+'&user='+ token,'name': user.name if user.name else user.username,'code': token},'email/verify2.html',[user.email],[],[],[])
            return Response(
                {   
                    "error": False,
                    "message": 'Authenticated',
                    # "cdsjfnbdsjfg" : str(tok.key)
                    # "details": detailspack(user),
                    # "code": code1
                }
            )
        except:
            return Response(
                {
                    "error": True,
                    "message": "Signup Successful but couldn't verify, Verify Later",
                    # "details": detailspack(user),
                    # "code": code1
                }
            )




@api_view(['POST'])
def sendagain(request): 
    try:
        tok = Token.objects.get(key=request.data['cdsjfnbdsjfg'])
    except:
        return Response(
            {
                "error": True,
                "status": "201",
                "message": "User not Found",
            }
        )
    try:
        # print('here 2 ')
        user = User.objects.get(id=tok.user.id)
        token = default_token_generator.make_token(user)
        # print(token)
        send_html_mail('Activate Your Account ',{'link': DOMAIN + '/verify/?token=' + str(tok.key)+'&user='+ token,'name': user.username,'code': token},'email/verify2.html',[user.email],[],[],[])
        return Response(
            {   
                "type": 'success',
                "status": "200",
                "cdsjfnbdsjfg" : str(tok.key)
            }
        )
    except:
        return Response(
            {
                "error": True,
                "status": "201",
                "message": "Signup Successful but couldn't verify, Verify Later",
            }
        )




@api_view(['POST'])
def verify2(request): 
    # if "hunaushdyuafr" in request.data:
        try:
            tok = Token.objects.get(key=request.data["cdsjfnbdsjfg"])
        except: 
            return Response({"error": True,"status": "210","message": 'User Not Found'})
        user = User.objects.get(id=tok.user.id)
        if default_token_generator.check_token(user,request.data["hunaushdyuafr"]) == True:
            user.email_confirmed = True
            if user.type == 'U':
                user.is_active = True
                user.verificationreputation += 1
            user.save()
            if user.refuser:
                refuser = User.objects.get(id=user.refuser.id)
                refuser.refreputation += 1
                refuser.save()
                send_html_mail('Account Activated',{'user': user.username,'refuser': user.refuser.username},'email/refer.html',[user.email],[user.refuser.email],[],[])
            else:
                if user.type == 'C':
                    send_html_mail('Account Verified',{'name': user.username},'email/confirm.html',[user.email],[],[],[])
                    return Response({"error": False,"status": "200","message": "Account Verified Successfully. Password will be mailed to you as soon as the admin will go through and activate your account or Admin will contact you shortly."})
                send_html_mail('Account Activated',{'name': user.username},'email/confirm.html',[user.email],[],[],[])
            return Response({"error": False,"status": "200","message": "Account Activated Successfully. You may login to SecuriumX now."})
        else:
            if user.email_confirmed:
                return Response({"error": True,"status": "210","message": "Link Expired. Account already verified"})
            else:
                return Response({"error": True,"status": "210","message": "Link Expired. Account not verified"})
    # else:
    #     return Response({"error": True,"status": "210","message": "User not Found"})

                
            
            

@api_view(['GET'])
def forgotsend(request,id): 
        try:
            user = User.objects.get(Q(username=id)|Q(email=id))
            tok = Token.objects.get(user=user)
        except:
            return Response({"error": True,"status": "210","message": 'User does not exists with this Email/Username'})
        try:
            token = default_token_generator.make_token(user)
        except:
            return Response({"status": "201","type":"error","error": True,"message": "Your Password Reset reached limit"})
        send_html_mail('Password Reset Link',{'link': DOMAIN + '/resetpassword?token=' + str(tok.key)+'&user='+ token,'name': user.username},'email/forgot.html',[user.email],[],[],[])
        return Response({"status": "200","type":"success","message": "A Password Reset Link has been mailed"})



@api_view(['POST'])
def forgotpassword(request): 
        # print(request.data)
    # if "hunaushdyuafr" in request.data:
        try:
            tok = Token.objects.get(key=request.data["cdsjfnbdsjfg"])
        except: 
            return Response({"error": True,"status": "210","message": "User not found"})
        user = User.objects.get(id=tok.user.id)
        if default_token_generator.check_token(user,request.data["hunaushdyuafr"]) == True:
            user.set_password(request.data['password'])
            user.reset = datetime.now()
            user.save()
            try:
                send_html_mail('Password Reset Successful',{'user': user.username},'email/change.html',[user.email],[],[],[])
            except: 
               print('Email Error at Forgot Confirm')
            return Response({"error": False,"status": "200"})
        else:
            return Response({"error": True,"status": "210","message": "Link has expired"})
    # else:
    #   #  print(request.data)
    #     return Response({"error": True,"status": "210","message": "Link has expired"})



















































# @api_view(['GET'])
# # # @authentication_classes([SessionAuthentication, TokenAuthentication])
# @authentication_classes([JWTTokenUserAuthentication])
# @permission_classes([IsAuthenticated])
# def verify(request,user=None): 
#     user = User.objects.get(id=request.user.id)
#     user.email_confirmed = True
#     user.save()
#     if user.refuser:
#         # print(user.refuser.username)
#         send_html_mail('Account Activated',{'user': user.username,'refuser': user.refuser.username},'email/refer.html',[user.email],[user.refuser.email],[],[])
#     else:
#         send_html_mail('Account Activated',{'name': user.username},'email/confirm.html',[user.email],[],[],[])
#     return Response(detailspack(user))




@api_view(['GET'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
def dashing(request,user=None): 
    userd = User.objects.get(id=request.user.id)
    # return Response(detailspack(userd))
    if userd.type == 'U':
        return Response(UserDashSerializer(userd, many=False, context={'request': request}).data)
    if userd.type == 'C':
        return Response(CompanyDashSerializer(userd, many=False, context={'request': request}).data)
    if userd.type == 'Ct':
        return Response(StaffDashSerializer(userd, many=False, context={'request': request}).data)



@api_view(['GET','POST'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
def profile(request,user=None): 
    # print(request.META)
    if request.method == 'GET':
        # print(request.user)
        if user==None:
            userd = User.objects.get(id=request.user.id)
            # return Response(detailspack(userd))
            if userd.type == 'U':
                return Response(SelfProfilingSerializer(userd, many=False, context={'request': request}).data)
            elif userd.type == 'C':
                return Response(CompanyProfilingSerializer(userd, many=False, context={'request': request}).data)
            else:
                return Response(CompanyProfilingSerializer(userd, many=False, context={'request': request}).data)
        else:
            try:
                userd = User.objects.get(username=user)
            except:
                return Response({'error': True, 'message': 'User Not Found'})
            # if userd.id != request.user.id:
            #     userd.visits +=1
                
            #     userd.save()
            if userd.type == 'U':
                userd.visits += 1
                userd.save()
                serializer=ProfilingSerializer(userd, many=False, context={'request': request})
                return Response(serializer.data)
            else:
                return Response({'error': True, 'message': 'Unauthorized'})
    if request.method == 'POST':
        # print(request.user)
        # print('editing')
        if user==None:
            userd = User.objects.get(id=request.user.id)
            userd.bio = request.data['bio'] if 'bio' in request.data else None
            userd.name = request.data['name'] if 'name' in request.data else None
            userd.save()
            return Response(SelfProfilingSerializer(userd, many=False, context={'request': request}).data)
        else:
            userd = User.objects.get(username=user)
            serializer=ProfilingSerializer(userd, many=False)
        return Response(serializer.data)



@api_view(['GET'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
def like(request,user=None): 
    # print(request.META)
    if request.method == 'GET':
        # print(request.user)
        if user==None:
            return Response(SelfProfilingSerializer(User.objects.get(id=request.user.id), many=False, context={'request': request}).data)
        else:
            try:
                userd = User.objects.get(username=user)
            except:
                return Response({'error': True, 'message': 'User Not Found'})
            if userd.type == 'U':
                user = User.objects.get(id=request.user.id)
                userd.likes.add(user)
                add_noti_single_email(userd, 'New Like',f"{user.name if user.name else user.username} gave you a like. Check out and like back.",avatar=user.photo.url if user.photo else None)
                serializer=ProfilingSerializer(userd, many=False, context={'request': request})
                return Response(serializer.data)
            else:
                return Response({'error': True, 'message': 'Unauthorized'})


@api_view(['POST'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
def report(request,user=None): 
    # print(request.META)
    if request.method == 'POST':
        # print(request.user)
        if user==None:
            return Response({'error': True, 'message': 'Unauthorized'})
        else:
            try:
                userd = User.objects.get(username=user)
            except:
                return Response({'error': True, 'message': 'User Not Found'})
            users = User.objects.filter(type__in=['A','S'])
            if request.data['anon']==True:
                main ='An Anonymous User has reported "'+userd.username+'" as '+request.data['name']+ ', stating the reason as '+request.data['reason']+'.'
            else:
                main =request.user.username+' has reported "'+userd.username+'" as '+request.data['name']+ ', stating the reason as '+request.data['reason']+'.'
            if userd.type == 'U':
                for use in users:
                    print(use.username)
                add_noti_multiple_email(users, 'Account Reported',main,link=f'/panel/back/user/{userd.id}/change/',type='U')
                return Response({'error': False, 'message': 'Account Reported Successfully'})
            else:
                return Response({'error': True, 'message': 'Unauthorized'})



@api_view(['GET','POST'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
def propic(request):
    if request.method == 'GET':
        user = User.objects.get(id=request.user.id)
        user.photo.delete()
        return Response(SelfProfilingSerializer(user, many=False, context={'request': request}).data)
    if request.method == 'POST':
        name = request.data['photo'].name
        if name.split('.')[1] not in ['png','jpg','jpeg']:
            return Response({'error': True,'message': 'Please Upload a proper image'})
        # print(name.split('.')[1])
        # print(request.data['photo'].name)
        user = User.objects.get(id=request.user.id)
        user.photo = request.data['photo']
        user.save()
        return Response(SelfProfilingSerializer(user, many=False, context={'request': request}).data)
        



@api_view(['GET','POST'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
def editlinks(request):
    if request.method == 'GET':
        return Response({"message": "Method not Found"})
    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        user.website = request.data['website']
        user.github = request.data['github']
        user.instagram = request.data['instagram']
        user.facebook = request.data['facebook']
        user.twitter = request.data['twitter']
        user.linkedin = request.data['linkedin']
        user.save()
        return Response(SelfProfilingSerializer(user, many=False, context={'request': request}).data)




@api_view(['POST'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
def change(request):
  #  print(request.data)
    user = authenticate(username=User.objects.get(id=request.user.id).username, password=request.data['old'])
    if user is not None:
        if len(request.data['new']) < 8:
            return Response({"error": True,"message": 'Password should contain atleast 8 characters'})
        if request.data['old'] == request.data['new']:
            return Response({"error": True,"message": 'New Password should not match old password'})
        user.set_password(request.data['new'])
        user.save()
        # send_html_mail('Password Changed',{'name': user.username},'email/change.html',[user.email],[],[],[])
        add_noti_single_email(user, 'Password Changed',"Your Password has been changed recently. If it was not you, then please contact the Admin")
        return Response({ "error": False, "message": 'Password Change was Successful' })
    else:
        return Response ({'error': True,'message': 'Old Password is Wrong'})



















@api_view(['GET','POST'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsCompany])
def staffs(request):
    if request.method == 'GET':
        user = User.objects.get(id=request.user.id)
        users = User.objects.filter(refuser=user)
        staffs = StaffSerializer(users, many=True)
        # logs = LogEntry.objects.filter()
        # print('user')
        return Response(staffs.data)    
    elif request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        newuser = User.objects.create_user(username=request.data['username'],email=request.data['email'],password=request.data['password'],name=request.data['name'],refuser=user, type='Ct')
        newuser.save()
        return Response({"message": "Staff Added Successfully","show": True})    























































@api_view(['GET'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
def usersbyrep(request,full=None): 
    # print(request.META)
    # print(request.user)
    if full==None:
        users = User.objects.filter(type='U',email_confirmed=True).order_by('-totalreputation')[:10]
        serializer=ProfileSerializer(users, many=True)
        users2 = User.objects.filter(type='U',email_confirmed=True).order_by('-upvotereputation')[:10]
        serializer2=ProfileSerializer(users2, many=True)
        users3 = User.objects.filter(type='U',email_confirmed=True).order_by('-refreputation')[:10]
        serializer3=ProfileSerializer(users3, many=True)
        total = User.objects.filter(type='U',email_confirmed=True).count()
        rank = 0
        for index, user in enumerate(User.objects.filter(type='U',email_confirmed=True).order_by('-totalreputation','-date_joined')):
            print(user.username)
            if user.id == request.user.id:
              #  print('found')
                rank = index
        # print(request.user.id)
        user = User.objects.get(id=request.user.id)
        return Response({'total':serializer.data,'upvotes': serializer2.data,'referral': serializer3.data,'comps': total, "rank": rank+1, "reputation": user.totalreputation,
        "programs" : ProgramSerializerShort(Program.objects.filter(managed=True)[:10],many=True).data })
    else:
        if full=='signup':
            users3 = User.objects.filter(type='U').order_by('-refreputation')[:100]
            serializer=ProfileSerializer(users3, many=True)
        elif full=='upvote':
            users2 = User.objects.filter(type='U').order_by('-upvotereputation')[:100]
            serializer=ProfileSerializer(users2, many=True)
        else:
            users = User.objects.filter(type='U').order_by('-totalreputation')[:100]
            serializer=ProfileSerializer(users, many=True)
        return Response(serializer.data) 

    

    

@api_view(['GET'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
def authusers(request): 
    # print(request.META)
  #  print(request.user)
    users = User.objects.filter(type='U').order_by('-totalreputation')[:5]
    serializer=ProfileSerializer(users, many=True)
    return Response({'current': 12,'users': serializer.data})

    

@api_view(['GET'])
@permission_classes([AllowAny])
def nonauthusers(request): 
    # print(request.META)
    # print(request.user)
    users = User.objects.filter(type='U').order_by('-totalreputation')[:5]
    serializer=ProfileSerializerPrivate(users, many=True)
    return Response(serializer.data)



    

    

@api_view(['POST'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
@authentication_classes([JWTTokenUserAuthentication])
# @permission_classes([IsAuthenticated])
def contact(request): 
    # print(request.META)
    try:
        user = User.objects.get(id=request.user.id)
        auth = True
    except User.DoesNotExist:
      #  print('No User')
        auth = False
    if auth:
        # send_html_mail('Message from Signed Up User',{},'',['adarshknt@gmail.com'],[])
        add_noti_single_email(user, 'Thank you for contacting SecuriumX',"Thank you for contacting us. We will get back to you as soon as possible")
        send_html_mail('New Message from Signed Up User',{'name': 'Adarsh','message': f"Message from {user.name if user.name else user.username}, <br /> Subject: {request.data['subject']} <br /> Message: {request.data['message']}"},'email/desc.html',["nikhilrai662@gmail.com","nikhilrai662@gmail.com","nikhilrai662@gmail.com"],[],[],[])
        return Response({'error': False,'message': 'Message sent Successfully','show': True})
    else:
        if len(request.data['email']) < 1 or len(request.data['name']) < 1:
            return Response({"error": True,"message": 'Please Add Everything Properly'})
        if not re.match(r"[^@]+@[^@]+\.[^@]+", request.data['email']):
            return Response({"error": True,"message": 'Enter a Valid Email'})
        # send_html_mail('Message from Anonymous User',{},'',['adarshknt@gmail.com'],[])
        send_html_mail('Thank you for contacting SecuriumX',{'name': request.data['name'],'message': f"Thank you for contacting us. We will get back to you as soon as possible"},'email/desc.html',[request.data['email']],[],[],[])
        send_html_mail('New Message from Anonymous User',{'name': 'Adarsh','message': f"Message from {request.data['name']} ({request.data['email']}), <br /> Subject: {request.data['subject']} <br /> Message: {request.data['message']}"},'email/desc.html',["nikhilrai662@gmail.com","nikhilrai662@gmail.com","nikhilrai662@gmail.com"],[],[],[])
        return Response({'error': False,'message': 'Message sent Successfully','show': True})
