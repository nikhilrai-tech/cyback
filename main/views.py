from django.http import HttpResponse
from django.shortcuts import render

from django.db.models import Q
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes 
from rest_framework.response import Response
# Create your views here.
from .models import *
from .serializers import *
from django.contrib.auth import get_user_model
from back.bviews import IsCompany
from other.notis import add_noti_multiple, add_noti_multiple_email, add_noti_single, add_noti_single_email
from rest_framework import permissions
from django.core.paginator import Paginator

User = get_user_model()







@api_view(['GET'])
@authentication_classes([JWTTokenUserAuthentication])
# @permission_classes([IsAuthenticated])
def getajobs(request,location='',type=0):
    # user = User.objects.get(id=request.user.id)
    if request.method == 'GET':
        jobs = Job.objects.all().order_by('-lastedited')
        job=JobSerializer(jobs, many=True)
        return Response({"jobs": job.data})
    













    

@api_view(['GET','POST'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
def getjobs(request,location='',type=0):
    user = User.objects.get(id=request.user.id)
    if request.method == 'GET':
        if user.type == 'U':
          #  print(type)
            locations = Job.objects.all().values_list("location", flat=True).distinct()
            print(locations)
            if len(location) > 0:
                fillocs = location.split(',')
            else:
                fillocs = locations
            if type==1 or type=='1':
              #  print('1')
                jobs = Job.objects.filter(location__in=fillocs,type='F').order_by('-lastedited')
            elif type==2 or type=='2':
              #  print('2')
                jobs = Job.objects.filter(location__in=fillocs,type='C').order_by('-lastedited')
            else:
              #  print('3')
                jobs = Job.objects.filter(location__in=fillocs).order_by('-lastedited')
            job=JobSerializer(jobs, many=True)
            return Response({"jobs": job.data,"locations": Job.objects.all().exclude(location='').values_list("location", flat=True).distinct()})
        if user.type == 'C':
            jobs = Job.objects.filter(posted_by=user).order_by('-lastedited')
            job=JobSerializer(jobs, many=True)
            return Response({"jobs": job.data})
        if user.type == 'Ct':
            jobs = Job.objects.filter(posted_by=user.refuser).order_by('-lastedited')
            job=JobSerializer(jobs, many=True)
            return Response({"jobs": job.data})
    if request.method == 'POST':
        if user.type == 'C':
            if Job.objects.filter(designation=request.data['title']).exists():
                return Response({"error": True,"message": "Job already exists with this title"})
            newjob = Job(posted_by=user, type=request.data['type'], designation=request.data['title'], description=request.data['description'], link=request.data['link'],
             remote=request.data['remote'], out=request.data['out'])
            newjob.save()
            if 'scopes' in request.data:
                for sc in request.data['scopes']:
                    scope = Scope.objects.get(id=sc)
                    newjob.scopes.add(scope)
            add_noti_multiple_email(User.objects.filter(is_active=True, type='U'),'Job Listing','New Job was added by '+user.name+' today. Go and check it out.','J','I','/jobs')
            # adminnoti
            job=JobSerializer(newjob, many=False)
            return Response({"job": job.data,"message": "Job successfully added","show": True})
        elif user.type == 'Ct':
            if Job.objects.filter(designation=request.data['title']).exists():
                return Response({"error": True,"message": "Job already exists with this title"})
            newjob = Job(posted_by=user.refuser, type=request.data['type'], designation=request.data['title'], description=request.data['description'], link=request.data['link'],
             remote=request.data['remote'], out=request.data['out'])
            newjob.save()
            if 'scopes' in request.data:
                for sc in request.data['scopes']:
                    scope = Scope.objects.get(id=sc)
                    newjob.scopes.add(scope)
            add_noti_multiple_email(User.objects.filter(is_active=True, type='U'),'Job Listing','New Job was added by '+user.refuser.name+' today. Go and check it out.','J','I','/jobs')
            # adminnoti
            job=JobSerializer(newjob, many=False)
            return Response({"job": job.data,"message": "Job successfully added","show": True})
        else:
            return Response({"scopes": "Unauthorized"})
    

















def check_report_perm(user, report):
    perm = False
    if user.type == 'U':
        perm = report.posted_by.id == user.id
    elif user.type == 'C':
        perm = report.program.posted_by.id == user.id
    elif user.type == 'Ct':
        perm = report.program.posted_by.id == user.refuser.id
    else:
        perm = False
    return report.disclosure or perm

































    

@api_view(['GET'])
@authentication_classes([JWTTokenUserAuthentication])
def getaprograms(request):
    if request.method == 'GET':
            programs = Program.objects.filter(deleted=False).order_by('-lastedited').exclude(type='PRI')
            paginator = Paginator(programs, 5)
            page_number = request.GET.get('page')
            programs2 = paginator.get_page(page_number)
            program=ProgramSerializer(programs2, many=True, context={'request': request})
            return Response({"programs": program.data, "pages": paginator.num_pages})
    else:
        return Response({"programs": "Unauthorized"})











    

@api_view(['GET', 'POST'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
def getprograms(request):
    user = User.objects.get(id=request.user.id)
    print('here')
    if request.method == 'GET':
        if user.type == 'U':
            programs = Program.objects.filter(
                Q(deleted=False) &
                ((Q(type=request.GET.get('type')) if 'type' in request.GET else Q(id__gte=0)) &
                 (Q(managed=True) if 'managed' in request.GET else Q(id__gte=0)) &
                 (Q(splitting=True) if 'splitting' in request.GET else Q(id__gte=0)))
            ).order_by('-lastedited').exclude(type='PRI')
            paginator = Paginator(programs, 5)
            page_number = request.GET.get('page')
            programs2 = paginator.get_page(page_number)
            program = ProgramSerializer(programs2, many=True, context={'request': request})
            return Response({"programs": program.data, "pages": paginator.num_pages})
        elif user.type == 'C':
            programs = Program.objects.filter(
                Q(posted_by=user, deleted=False) &
                ((Q(type=request.GET.get('type')) if 'type' in request.GET else Q(id__gte=0)) &
                 (Q(managed=True) if 'managed' in request.GET else Q(id__gte=0)) &
                 (Q(splitting=True) if 'splitting' in request.GET else Q(id__gte=0)))
            ).order_by('-lastedited').exclude(type='PRI')
            paginator = Paginator(programs, 5)
            page_number = request.GET.get('page')
            programs2 = paginator.get_page(page_number)
            program = ProgramSerializer(programs2, many=True, context={'request': request})
            return Response({"programs": program.data, "pages": paginator.num_pages})
        elif user.type == 'Ct':
            programs = Program.objects.filter(
                Q(posted_by=user.refuser, deleted=False) &
                ((Q(type=request.GET.get('type')) if 'type' in request.GET else Q(id__gte=0)) &
                 (Q(managed=True) if 'managed' in request.GET else Q(id__gte=0)) &
                 (Q(splitting=True) if 'splitting' in request.GET else Q(id__gte=0)))
            ).order_by('-lastedited').exclude(type='PRI')
            paginator = Paginator(programs, 5)
            page_number = request.GET.get('page')
            programs2 = paginator.get_page(page_number)
            program = ProgramSerializer(programs2, many=True, context={'request': request})
            return Response({"programs": program.data, "pages": paginator.num_pages})
        else:
            return Response({"programs": "Unauthorized"})
    elif request.method == 'POST':
        print(request.data)
        external = request.data.get('external')
        print("External Link:", external)
        # if externallink:
        #     external = True
        # else:
        #     external = False
        if user.type in ['C', 'Ct']:
            if len(request.data['title']) < 1 or len(request.data['type']) < 1:
                return Response({"error": True, "message": "Please add everything properly"})
            if Program.objects.filter(title=request.data['title']).exists():
                return Response({"error": True, "message": "Program already exists with this title"})
            new_program_data = {
        'title': request.data['title'],
        'type': request.data['type'],
        'policy': request.data.get('description', ''),
        'lowreward': request.data.get('low', 0),
        'midreward': request.data.get('mid', 0),
        'highreward': request.data.get('high', 0),
        'criticreward': request.data.get('critic', 0),
        'managed': request.data.get('managed', False),
        'splitting': request.data.get('splitting', False),
        'external': external,
    }
            if user.type == 'C':
                new_program_data['posted_by'] = user
            elif user.type == 'Ct':
                new_program_data['posted_by'] = user.refuser

            new_program = Program.objects.create(**new_program_data)

            if request.data['type'] == 'PRI':
                for username in request.data.get('users', []):
                    try:
                        user_to_add = User.objects.get(username__iexact=username)
                        new_program.subscribed.add(user_to_add)
                    except User.DoesNotExist:
                        print(f"User '{username}' not found.")

            if 'scopes' in request.data:
                for scope_id in request.data['scopes']:
                    try:
                        scope = Scope.objects.get(id=scope_id)
                        new_program.scopes.add(scope)
                    except Scope.DoesNotExist:
                        print(f"Scope with ID '{scope_id}' not found.")

            program_serializer = ProgramSerializer(new_program, context={'request': request})
            return Response({"program": program_serializer.data, "message": "Program successfully added", "show": True})
        else:
            return Response({"scopes": "Unauthorized"})
            

    

@api_view(['GET'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
def filteredprograms(request,type=None):
    user = User.objects.get(id=request.user.id)
    # users = User.objects.filter(refuser__in=[user])
    # print(users)
    if request.method == 'GET':
        if user.type == 'U':
            programs = Program.objects.filter(type='PRI',subscribed__in=[user.id], deleted=False).order_by('-lastedited') if type=='private' else Program.objects.filter(subscribed__in=[user.id]).order_by('-lastedited').exclude(type='PRI')
            program=ProgramSerializer(programs, many=True, context={'request': request})
            return Response({"programs": program.data})
        elif user.type == 'C':
            programs = Program.objects.filter(type='PRI',posted_by=user, deleted=False).order_by('-lastedited')
            program=ProgramSerializer(programs, many=True, context={'request': request})
            return Response({"programs": program.data})
        elif user.type == 'Ct':
            programs = Program.objects.filter(type='PRI',posted_by=user.refuser, deleted=False).order_by('-lastedited')
            program=ProgramSerializer(programs, many=True, context={'request': request})
            return Response({"programs": program.data})
        else:
            return Response({"programs": "Unauthorized"})
    # if request.method == 'POST':
    #     if user.type == 'C':
    #         if Program.objects.filter(title=request.data['title']).exists():
    #             return Response({"error": True,"message": "Program already exists with this title"})
    #         newprogram = Program(posted_by=user, type=request.data['type'], title=request.data['title'], policy=request.data['description'], lowreward=request.data['low'], 
    #         midreward=request.data['mid'],highreward=request.data['high'],criticreward=request.data['critic'], managed=request.data['managed'], splitting=request.data['splitting'])
    #         newprogram.save()
    #         if 'scopes' in request.data:
    #             for sc in request.data['scopes']:
    #                 scope = Scope.objects.get(id=sc)
    #                 newprogram.scopes.add(scope)
    #         program=ProgramSerializer(newprogram, many=False, context={'request': request})
    #         return Response({"program": program.data,"message": "Program successfully added","show": True})
    #     elif user.type == 'Ct':
    #         if Program.objects.filter(title=request.data['title']).exists():
    #             return Response({"error": True,"message": "Program already exists with this title"})
    #         newprogram = Program(posted_by=user.refuser, type=request.data['type'], title=request.data['title'], policy=request.data['description'], lowreward=request.data['low'], 
    #         midreward=request.data['mid'],highreward=request.data['high'],criticreward=request.data['critic'], managed=request.data['managed'], splitting=request.data['splitting'])
    #         newprogram.save()
    #         if 'scopes' in request.data:
    #             for sc in request.data['scopes']:
    #                 scope = Scope.objects.get(id=sc)
    #                 newprogram.scopes.add(scope)
    #         program=ProgramSerializer(newprogram, many=False, context={'request': request})
    #         return Response({"program": program.data,"message": "Program successfully added","show": True})
    #     else:
    #         return Response({"scopes": "Unauthorized"})
    

@api_view(['GET','POST'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
def program(request, pid):
    user = User.objects.get(id=request.user.id)
    pid = pid.replace('+', ' ')

    if request.method == 'GET':
        try:
            programs = Program.objects.get(title=pid, deleted=False)
        except Program.DoesNotExist:
            return Response({'error': True, 'message': 'Program not found'})

        serializer = ProgramSerializerMore(programs, many=False, context={'request': request})
        response_data = serializer.data
        if user.type == 'U' and (programs.type != 'PRI' or user in programs.subscribed.all()):
            return Response(response_data)
        elif user.type == 'C' and (programs.type != 'PRI' or user.id == programs.posted_by.id):
            return Response(response_data)
        elif user.type == 'Ct' and (programs.type != 'PRI' or user.refuser.id == programs.posted_by.id):
            return Response(response_data)
        else:
            return Response({"error": True, "message": "Program Not Found", "program": "Unauthorized"})
    if request.method == 'POST':
        try:
            programs = Program.objects.get(title=pid, deleted=False)
        except:
            return Response({'error': True,'message': 'Program not found'})
        if user.type == 'U' and (programs.type != 'PRI' or user in programs.subscribed.all()):
            program=ProgramSerializerMore(programs, many=False, context={'request': request})
            return Response(program.data)
        elif user.type == 'C' and (programs.type != 'PRI' or user.id== programs.posted_by.id):
            print(request.data)
            programs.title = request.data['title']
            programs.type = request.data['type']
            programs.policy = request.data['description']
            programs.lowreward = request.data['low']
            programs.midreward = request.data['mid']
            programs.highreward = request.data['high']
            programs.criticreward = request.data['critic']
            programs.managed = request.data['managed']
            programs.splitting = request.data['splitting']
            programs.save()
            program=ProgramSerializerMore(programs, many=False, context={'request': request})
            return Response({"program":program.data, "message": "Successfully Edited the Program", "show": True})
        elif user.type == 'Ct' and (programs.type != 'PRI' or user.refuser.id== programs.posted_by.id):
            print(request.data)
            programs.title = request.data['title']
            programs.type = request.data['type']
            programs.policy = request.data['description']
            programs.lowreward = request.data['low']
            programs.midreward = request.data['mid']
            programs.highreward = request.data['high']
            programs.criticreward = request.data['critic']
            programs.managed = request.data['managed']
            programs.splitting = request.data['splitting']
            programs.save()
            program=ProgramSerializerMore(programs, many=False, context={'request': request})
            return Response({"program":program.data, "message": "Successfully Edited the Program", "show": True})
        # elif user.type in ['U','C','Ct'] and (programs.type != 'PRI' or user in programs.subscribed.all() or user==programs.postedby.....):
            program=ProgramSerializerMore(programs, many=False, context={'request': request})
            return Response(program.data)
        else:
            return Response({"error": True,"message": "Program Not Found","program": "Unauthorized"})
    

    

@api_view(['GET'])
@authentication_classes([JWTTokenUserAuthentication])
# @permission_classes([IsAuthenticated])
def aprogram(request, pid):
    # user = User.objects.get(id=request.user.id)
    # users = User.objects.filter(refuser__in=[user])
    # print(users)
    # print(pid)
    pid = pid.replace('+',' ')
    # print(pid)
    if request.method == 'GET':
        try:
            programs = Program.objects.get(title=pid, deleted=False)
        except:
            return Response({'error': True,'message': 'Program not found'})
        # if user.type == 'U' and (programs.type != 'PRI' or user in programs.subscribed.all()):
        #     program=ProgramSerializerMore(programs, many=False, context={'request': request})
        #     return Response(program.data)
        # elif user.type == 'C' and (programs.type != 'PRI' or user.id== programs.posted_by.id):
        #     program=ProgramSerializerMore(programs, many=False, context={'request': request})
        #     return Response(program.data)
        # elif user.type == 'Ct' and (programs.type != 'PRI' or user.refuser.id== programs.posted_by.id):
        program=ProgramSerializerMore(programs, many=False, context={'request': request})
        return Response(program.data)
        # elif user.type in ['U','C','Ct'] and (programs.type != 'PRI' or user in programs.subscribed.all() or user==programs.postedby.....):
            # program=ProgramSerializerMore(programs, many=False, context={'request': request})
            # return Response(program.data)
        # else:
        #     return Response({"error": True,"message": "Program Not Found","program": "Unauthorized"})
    
    

@api_view(['GET'])
@authentication_classes([JWTTokenUserAuthentication])
# @permission_classes([IsAuthenticated])
def dprogram(request, pid):
    # user = User.objects.get(id=request.user.id)
    # users = User.objects.filter(refuser__in=[user])
    # print(users)
    # print(pid)
    pid = pid.replace('+',' ')
    # print(pid)
    if request.method == 'GET':
        try:
            programs = Program.objects.get(title=pid, deleted=False)
        except:
            return Response({'error': True,'message': 'Program not found'})
        # if user.type == 'U' and (programs.type != 'PRI' or user in programs.subscribed.all()):
        #     program=ProgramSerializerMore(programs, many=False, context={'request': request})
        #     return Response(program.data)
        # elif user.type == 'C' and (programs.type != 'PRI' or user.id== programs.posted_by.id):
        #     program=ProgramSerializerMore(programs, many=False, context={'request': request})
        #     return Response(program.data)
        # elif user.type == 'Ct' and (programs.type != 'PRI' or user.refuser.id== programs.posted_by.id):
        programs.delete()
        return Response({"message": "Program Successfully Deleted","show": True})
        # elif user.type in ['U','C','Ct'] and (programs.type != 'PRI' or user in programs.subscribed.all() or user==programs.postedby.....):
            # program=ProgramSerializerMore(programs, many=False, context={'request': request})
            # return Response(program.data)
        # else:
        #     return Response({"error": True,"message": "Program Not Found","program": "Unauthorized"})
    


    

@api_view(['POST'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsCompany])
def background(request, pid):
    pid = pid.replace('+',' ')
    user = User.objects.get(id=request.user.id)
    if user.type == 'C':
        program = Program.objects.get(title=pid)
        name = request.data['photo'].name
        if name.split('.')[1] not in ['png','jpg','jpeg']:
            return Response({'error': True,'message': 'Please Upload a proper image'})
        program.background = request.data['photo']
        program.save()
        return Response({"error": False})
    



@api_view(['GET'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
def favorite(request,prog=None,type=None): 
    # print(request.META)
    prog = prog.replace('+',' ')
    if request.method == 'GET':
        # print(request.user)
        if prog==None or type==None:
            return Response({'error': True, 'message': 'Unauthorized'})
        else:
            try:
                program = Program.objects.get(title=prog)
            except:
                return Response({'error': True, 'message': 'Program Not Found'})
            user = User.objects.get(id=request.user.id)
            if user.type == 'U':
                if type=='1':
                    program.subscribed.add(user)
                    add_noti_single(user, 'Added to Favourites',f"{program.title} was successfully added to your favourites.",link=f'/p/?{program.title}',avatar=program.background.url if program.background else None)
                    return Response({"message": "Added Program to Favorites","show": True})
                elif type=='2':
                    program.subscribed.remove(user)
                    add_noti_single(user, 'Removed from Favourites',f"{program.title} was successfully removed from your favourites.",ntype='E',link=f'/p/?{program.title}',avatar=program.background.url if program.background else None)
                    return Response({"message": "Removed Program from Favorites","show": True})
                else:
                    return Response({"message": "Something Went Wrong","show": True})
            else:
                return Response({'error': True, 'message': 'Unauthorized'})



    

































































@api_view(['GET','POST'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsCompany])
def getscopes(request):
    if request.method == 'GET':
        user = User.objects.get(id=request.user.id)
        if user.type == 'C':
            scope = Scope.objects.filter(company=user)
            scopes=ScopeSerializer(scope, many=True)
            return Response({"scopes": scopes.data, "users": BaseSerializer(User.objects.filter(type='U'), many=True).data})
        elif user.type == 'Ct':
            scope = Scope.objects.filter(company=user.refuser)
            scopes=ScopeSerializer(scope, many=True)
            return Response({"scopes": scopes.data, "users": BaseSerializer(User.objects.filter(type='U'), many=True).data})
        else:
            print(user.type)
            return Response({"scopes": "Unauthorized"})
    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        if user.type == 'C':
            scoped = Scope(company=user, type=request.data['type'], severity=request.data['severity'], tags=request.data['tags'], out=request.data['out'], bounty=request.data['bounty'], domain=request.data['domain'])
            scoped.save()
            scope = Scope.objects.filter(company=user)
            scopes=ScopeSerializer(scope, many=True)
            return Response({"scopes": scopes.data,"message": "Scope successfully added","show": True})
        elif user.type == 'Ct':
            scoped = Scope(company=user.refuser, type=request.data['type'], severity=request.data['severity'], tags=request.data['tags'], out=request.data['out'], bounty=request.data['bounty'], domain=request.data['domain'])
            scoped.save()
            scope = Scope.objects.filter(company=user.refuser)
            scopes=ScopeSerializer(scope, many=True)
            return Response({"scopes": scopes.data,"message": "Scope successfully added","show": True})
        else:
            return Response({"scopes": "Unauthorized"})


            

    

@api_view(['GET','POST'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsCompany])
def scope(request,sid):
    if request.method == 'GET':
        user = User.objects.get(id=request.user.id)
        if user.type == 'C':
            scope = Scope.objects.get(id=sid)
            scope.delete()
            return Response({"error": False})
        elif user.type == 'Ct':
            scope = Scope.objects.get(id=sid)
            scope.delete()
            return Response({"error": False})
        else:
            return Response({"scopes": "Unauthorized"})
    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        if user.type == 'C':
            scope = Scope.objects.get(id=sid)
            scope.type = request.data['type']
            scope.severity = request.data['severity'] if 'severity' in request.data else None
            scope.tags = request.data['tags'] if 'tags' in request.data else ''
            scope.out = request.data['out'] if 'out' in request.data else False
            scope.bounty = request.data['bounty'] if 'bounty' in request.data else False
            scope.domain = request.data['domain']
            scope.save()
            scopes=ScopeSerializer(scope, many=False)
            return Response({"scope": scopes.data,"message": "Scope successfully edited","show": True})
        elif user.type == 'Ct':
            scope = Scope.objects.get(id=sid)
            scope.type = request.data['type']
            scope.severity = request.data['severity'] if 'severity' in request.data else None
            scope.tags = request.data['tags'] if 'tags' in request.data else ''
            scope.out = request.data['out'] if 'out' in request.data else False
            scope.bounty = request.data['bounty'] if 'bounty' in request.data else False
            scope.domain = request.data['domain']
            scope.save()
            scopes=ScopeSerializer(scope, many=True)
            return Response({"scope": scopes.data,"message": "Scope successfully edited","show": True})
        else:
            return Response({"scope": "Unauthorized"})




            
            









































            



@api_view(['GET','POST'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
def reportpl(request, pid=None):
    user = User.objects.get(id=request.user.id)
    # users = User.objects.filter(refuser__in=[user])
    # print('entered here')
    # print(pid)
    if pid:
        pid = pid.replace('+',' ')
    # print(pid)
    if request.method == 'GET':
        if pid==None:
            if user.type == 'U':
                reports = Report.objects.filter(posted_by=user, deleted=False).order_by('-lastedited')
                report=ReportSerializerShort(reports, many=True, context={'request': request})
                return Response({"reports": report.data})
            elif user.type == 'C':
                programs = Program.objects.filter(posted_by=user, deleted=False).order_by('-lastedited')
                reports = Report.objects.filter(program__in=programs, deleted=False).order_by('-lastedited')
                report=ReportSerializerShort(reports, many=True, context={'request': request})
                return Response({"reports": report.data})
            elif user.type == 'Ct':
                programs = Program.objects.filter(posted_by=user.refuser, deleted=False).order_by('-lastedited')
                reports = Report.objects.filter(program__in=programs, deleted=False).order_by('-lastedited')
                report=ReportSerializerShort(reports, many=True, context={'request': request})
                return Response({"reports": report.data})
            else:
                return Response({"reports": "Unauthorized"})
    if request.method == 'POST':
        if user.type == 'U':
            # print(request.data['impact'])
          #  print(request.data)
            if 'photo0' in request.data:
                # print(request.data['photo1'])
                name = request.data['photo0'].name
                if name.split('.')[1] not in ['png','jpg','jpeg']:
                    return Response({'error': True,'message': 'Please Upload a proper image'})
            if 'photo1' in request.data:
                # print(request.data['photo1'])
                name = request.data['photo1'].name
                if name.split('.')[1] not in ['png','jpg','jpeg']:
                    return Response({'error': True,'message': 'Please Upload a proper image'})
            if 'photo2' in request.data:
                # print(request.data['photo1'])
                name = request.data['photo2'].name
                if name.split('.')[1] not in ['png','jpg','jpeg']:
                    return Response({'error': True,'message': 'Please Upload a proper image'})
            if 'title' in request.data:
                if len(request.data['title']) < 1:
                    return Response({'error': True,'message': 'Please Enter a title'})
            else:
                return Response({'error': True,'message': 'Please Enter a title'})
            try:
                program = Program.objects.get(title=pid)
            except:
                return Response({'error': True,'message': 'Program not found'})
            try:
                scope = Scope.objects.get(id=request.data['scope'])
            except:
                return Response({'error': True,'message': 'Asset not found'})
            if 'weakness' in request.data:
                if len(request.data['weakness']) < 1:
                    return Response({'error': True,'message': 'Please Enter a Weakness'})
            # if Report.objects.filter(title=request.data['title']).exists():
            #     return Response({"error": True,"message": "Report already exists with this title"})
            rep = Report(program=program, asset= scope, title=request.data['title'], impact=request.data['impact'], description=request.data['description'], 
            severity=request.data['severity'], weakness=request.data['weakness'], posted_by = user,
            photo0=request.data['photo0'] if 'photo0' in request.data else None, 
            photo1=request.data['photo1'] if 'photo1' in request.data else None, 
            photo2=request.data['photo2'] if 'photo2' in request.data else None,)
            rep.save()
            add_noti_single_email(program.posted_by, 'Bug Reported','A new bug was reported by '+user.name+' for the Program '+program.title+'. Go and check it out.','R','I','/inbox?report='+str(rep.id))
            add_noti_multiple_email(User.objects.filter(is_active=True, type='Ct', refuser=program.posted_by),'Bug Reported','A new bug was reported by '+user.name+' for the Program '+program.title+'. Go and check it out.','R','I','/inbox?report='+str(rep.id))
            # programs = Report(title=request.da)
            # program=ProgramSerializerMore(programs, many=False, context={'request': request})
            # return Response(program.data)
            return Response({"show": True,"message": "Report Successfully Added"})
        else:
            return Response({"report": "Unauthorized"})


@api_view(['GET','POST'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
def specreport(request, rid=None,type='1'):
    user = User.objects.get(id=request.user.id)
    report = Report.objects.get(id=rid, deleted=False)
    if not check_report_perm(user, report):
        return Response({"report": "Unauthorized","error": True,"message": "Report Unauthorized"})
    # if rid:
    #     rid = rid.replace('+',' ')
    # print(pid)
    if request.method == 'GET':
        reportspec=ReportSerializerLong(report, many=False, context={'request': request})
        comment = Comment.objects.filter(report=report)
        comments = CommentSerializer(comment, many=True, context={'request': request} ) 
        return Response({"report": reportspec.data, "timeline": comments.data})
    if request.method == 'POST':
        if user.type == 'U':
            if type == '1':
                newcomment = Comment(report=report, posted_by=user, body=request.data['body'])
                newcomment.save()
                # return Response({"show": True,"message": "Comment Successfully Added"})
            elif type == '2':
                newcomment = Comment(report=report, posted_by=user, type='D',request=True)
                newcomment.save()
                # return Response({"show": True,"message": "Request Successfully Sent"})
            elif type == '3':
                newcomment = Comment(report=report, posted_by=user, type='A',request=True)
                newcomment.save()
                # return Response({"show": True,"message": "Request Successfully Sent"})
            else:
                return Response({"error": True,"message": "Something went wrong"})
            reportspec=ReportSerializerLong(report, many=False, context={'request': request})
            comment = Comment.objects.filter(report=report)
            comments = CommentSerializer(comment, many=True, context={'request': request} ) 
            return Response({"report": reportspec.data, "timeline": comments.data})
            return Response({"show": True,"message": "Comment Successfully Added"})
        elif user.type == 'Ct' or user.type == 'C' :
            messages = None
            if type == '1':
                newcomment = Comment(report=report, posted_by=user, body=request.data['body'])
                newcomment.save()
                # return Response({"show": True,"message": "Comment Successfully Added"})
            elif type == '2':
                newcomment = Comment(report=report, posted_by=user, type='D')
                newcomment.save()
                report.disclosure = True
                report.save()
                messages = 'Report was successfully made Public '
            elif type == '3':
                # newcomment = Comment(report=report, posted_by=user, type='A',request=True)
                # newcomment.save()
                return Response({"show": True,"message": "Request Successfully Sent"})
            elif type == '4':
                newcomment = Comment(report=report, posted_by=user, type='D2')
                newcomment.save()
                report.disclosure = False
                report.save()
                messages = 'Report Hidden Successfully'
                # return Response({"show": True,"message": "Request Successfully Sent"})
            elif type == '5':
                newcomment = Comment(report=report, posted_by=user, type='T',body=request.data['thanks'])
                newcomment.save()
                thanks = Thanks(fro=user,to=report.posted_by,description=request.data['description'],reputation=request.data['thanks'])
                thanks.save()
                thanked = User.objects.get(id=report.posted_by.id)
                thanked.otherreputation += request.data['thanks']
                thanked.save()
                program = Program.objects.get(id=report.program.id)
                program.thanks.add(thanks)
                program.save()
                add_noti_single_email(report.posted_by, 'A Thank you!','You received thanks of '+str(request.data['thanks'])+' from '+user.name+' for the Report '+report.title+'. Go and check it out.','R','I','/inbox?report='+str(report.id))
                messages = 'Thanks was successfully sent'
            else:
                return Response({"error": True,"message": "Something went wrong"})
            reportspec=ReportSerializerLong(report, many=False, context={'request': request})
            comment = Comment.objects.filter(report=report)
            comments = CommentSerializer(comment, many=True, context={'request': request} ) 
            resp = {"report": reportspec.data, "timeline": comments.data}
            if messages:
                resp["message"] = messages
                resp["show"] = True
            # print(resp)
            return Response(resp)
            return Response({"show": True,"message": "Comment Successfully Added"})
        else:
            return Response({"report": "Unauthorized"})



























            
@api_view(['GET'])
# @authentication_classes([JWTTokenUserAuthentication])
# @permission_classes([IsAuthenticated])
def apublicreport(request, rid=None,type=None):
    print('here')
    if rid==None:
        if request.method == 'POST':
            return Response({"error": True,"message": "Reports Unauthorized"})
        reports = Report.objects.filter(disclosure=True, deleted=False)
        reportspec=PublicReportSerializerShort(reports, many=True, context={'request': request})
        return Response(reportspec.data)
    # user = User.objects.get(id=request.user.id)
    report = Report.objects.get(id=rid, deleted=False)
    if not report.disclosure:
        return Response({"report": "Unauthorized","error": True,"message": "Report Unauthorized"})
    if request.method == 'GET':
        reportspec=PublicReportSerializerLong(report, many=False, context={'request': request})
        comment = Comment.objects.filter(report=report)
        comments = CommentSerializer(comment, many=True, context={'request': request} ) 
        return Response({"report": reportspec.data, "timeline": comments.data})
    if request.method == 'POST':
            return Response({"report": "Unauthorized"})
















            
@api_view(['GET','POST'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
def publicreport(request, rid=None,type=None):
    if rid==None:
        if request.method == 'POST':
            return Response({"error": True,"message": "Reports Unauthorized"})
        reports = Report.objects.filter(disclosure=True, deleted=False)
        reportspec=PublicReportSerializerShort(reports, many=True, context={'request': request})
        return Response(reportspec.data)
    user = User.objects.get(id=request.user.id)
    report = Report.objects.get(id=rid, deleted=False)
    if not check_report_perm(user, report):
        return Response({"report": "Unauthorized","error": True,"message": "Report Unauthorized"})
    if request.method == 'GET':
        reportspec=PublicReportSerializerLong(report, many=False, context={'request': request})
        comment = Comment.objects.filter(report=report)
        comments = CommentSerializer(comment, many=True, context={'request': request} ) 
        return Response({"report": reportspec.data, "timeline": comments.data})
    if request.method == 'POST':
        if user.type == 'U':
            if type == None:
                print(user in report.upvotes.all())
                if user in report.upvotes.all():
                    report.upvotes.remove(user)
                    report.save()
                else:
                    report.upvotes.add(user)
                    report.save()
                return Response({"error": False})
                return Response({"report": reportspec.data, "timeline": comments.data})
            # if type == '1':
            #     newcomment = Comment(report=report, posted_by=user, body=request.data['body'])
            #     newcomment.save()
            #     # return Response({"show": True,"message": "Comment Successfully Added"})
            # elif type == '2':
            #     newcomment = Comment(report=report, posted_by=user, type='D',request=True)
            #     newcomment.save()
            #     # return Response({"show": True,"message": "Request Successfully Sent"})
            # elif type == '3':
            #     newcomment = Comment(report=report, posted_by=user, type='A',request=True)
            #     newcomment.save()
            #     # return Response({"show": True,"message": "Request Successfully Sent"})
            # else:
            #     return Response({"error": True,"message": "Report Unauthorized"})
            # reportspec=ReportSerializerLong(report, many=False, context={'request': request})
            # comment = Comment.objects.filter(report=report)
            # comments = CommentSerializer(comment, many=True, context={'request': request} ) 
            # return Response({"report": reportspec.data, "timeline": comments.data})
            return Response({"show": True,"message": "Comment Successfully Added"})
        elif user.type == 'Ct' or user.type == 'C' :
            if type == None:
                print(user in report.upvotes.all())
                if user in report.upvotes.all():
                    report.upvotes.remove(user)
                    report.save()
                else:
                    report.upvotes.add(user)
                    report.save()
                return Response({"error": False})
            # messages = None
            # if type == '1':
            #     newcomment = Comment(report=report, posted_by=user, body=request.data['body'])
            #     newcomment.save()
            #     # return Response({"show": True,"message": "Comment Successfully Added"})
            # elif type == '2':
            #     newcomment = Comment(report=report, posted_by=user, type='D')
            #     newcomment.save()
            #     report.disclosure = True
            #     report.save()
            #     messages = 'Report was successfully made Public '
            # elif type == '3':
            #     # newcomment = Comment(report=report, posted_by=user, type='A',request=True)
            #     # newcomment.save()
            #     return Response({"show": True,"message": "Request Successfully Sent"})
            # elif type == '4':
            #     newcomment = Comment(report=report, posted_by=user, type='D2')
            #     newcomment.save()
            #     report.disclosure = False
            #     report.save()
            #     messages = 'Report Hidden Successfully'
            #     # return Response({"show": True,"message": "Request Successfully Sent"})
            # elif type == '5':
            #     newcomment = Comment(report=report, posted_by=user, type='T',body=request.data['thanks'])
            #     newcomment.save()
            #     thanks = Thanks(fro=user,to=report.posted_by,description=request.data['description'],reputation=request.data['thanks'])
            #     thanks.save()
            #     thanked = User.objects.get(id=report.posted_by.id)
            #     thanked.otherreputation += request.data['thanks']
            #     thanked.save()
            #     program = Program.objects.get(id=report.program.id)
            #     program.thanks.add(thanks)
            #     program.save()
            #     messages = 'Thanks was successfully sent'
            # else:
            #     return Response({"error": True,"message": "Report Unauthorized"})
            # reportspec=ReportSerializerLong(report, many=False, context={'request': request})
            # comment = Comment.objects.filter(report=report)
            # comments = CommentSerializer(comment, many=True, context={'request': request} ) 
            # resp = {"report": reportspec.data, "timeline": comments.data}
            # if messages:
            #     resp["message"] = messages
            #     resp["show"] = True
            # print(resp)
            # return Response(resp)
            # return Response({"show": True,"message": "Comment Successfully Added"})
        else:
            return Response({"report": "Unauthorized"})