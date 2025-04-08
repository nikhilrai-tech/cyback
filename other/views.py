from decimal import Decimal
from django.shortcuts import render
import json
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes 
from rest_framework.response import Response
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from main.models import Report, Comment
from django.utils import timezone
from honeb.settings import APP_DOMAIN
# Create your views here.
import razorpay
import requests
import re
from back.serializers import SelfProfilingSerializer
from django.contrib.auth import get_user_model
from back.bviews import IsCompany, IsUser

from other.models import Notification
from rest_framework import serializers

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render

from other.notis import add_noti_single, add_noti_single_email
# from back.serializers import BaseSerializer
from .models import *

User = get_user_model()

razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

razorpay_client.set_app_details({"title" : "Cyber3ra Bounty", "version" : "2.1.2"})

class NotiSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_type_display')
    class Meta:
        model = Notification
        fields = '__all__'
        depth = 2


@api_view(['GET','POST'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
def getnotis(request):
    if request.method == 'GET':
        user = User.objects.get(id=request.user.id)
        notis = Notification.objects.filter(of=user).order_by('seen','-pdate')
        noti = NotiSerializer(notis,many=True)
        return Response(noti.data)
    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        notis = Notification.objects.filter(of=user,seen=True)
        for n in notis:
            notic = Notification.objects.get(id=n.id)
            notic.delete()
        notis = Notification.objects.filter(of=user)
        noti = NotiSerializer(notis,many=True)
        return Response(noti.data)

    

@api_view(['GET'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
def markread(request, nid):
    noti = Notification.objects.get(id=nid)
    noti.seen = True
    noti.save()
    return Response("success")










    

@api_view(['POST'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsCompany])
def paybounty(request, rid):
    user = User.objects.get(id=request.user.id)
    report = Report.objects.get(id=rid)
    if report.program.posted_by not in [user.refuser, user] and report.disclosure == False:
        return Response({"report": "Unauthorized"})
  #  print(request.data)
    if not 'amount' in request.data:
        return Response({"error": True,"message": "Please add amount"})
    # user = User.objects.get(id=request.user.id)
    
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=int(float(request.data['amount'])*100),currency='INR', payment_capture='0'))
    
    # order id of newly created order.
 
    newcomment = Comment(report=report, posted_by=user, type='Ri',body=request.data['amount'])
    newcomment.save()
    bounty = Bounty(fro=user,to=report.posted_by,description=razorpay_order['id'],amount=request.data['amount'], report=report)
    bounty.save()
    return Response({'order_id' : razorpay_order['id'], 'key': settings.RAZOR_KEY_ID, 'amount': int(float(request.data['amount'])*100), 'currency': 'INR',
    'callback_url' : APP_DOMAIN+'/app/user/paymenthandler/'+razorpay_order['id'],'name': 'Cyber3ra Bounty',"image": "/cyber3ra.svg","remember_customer": True, "description": "Pay Bounty to User",
    "theme": { "color": "#0f1724","backdrop_color": "#000000ab" },"prefill": { "name": user.name, "email": user.email, "contact": user.contact if user.contact else ''
    }})   
    return render(request, 'index.html', context=context)
 
 
@api_view(['POST'])
# @authentication_classes([JWTTokenUserAuthentication])
# @permission_classes([IsCompany])
def paymenthandler(request, pid):
    bounty = Bounty.objects.get(description=pid)
    user = User.objects.get(id=bounty.fro.id)
 
    # try:
        
    # get the required parameters from post request.
    payment_id = request.data['razorpay_payment_id']
    params_dict = {
        'razorpay_order_id': request.data['razorpay_order_id'],
        'razorpay_payment_id': payment_id,
        'razorpay_signature': request.data['razorpay_signature']
        # 
    }
    # print(params_dict)
    # verify the payment signature.
    try:
        result = razorpay_client.utility.verify_payment_signature(
            params_dict)

        try:
            razorpay_client.payment.capture(payment_id, bounty.amount*100)
            bounty.paid = True
            bounty.save()
            # print('success')
            newcomment = Comment(report=bounty.report, posted_by=user, type='Rs',body=bounty.amount)
            newcomment.save()
            add_noti_single_email(bounty.to,'New Bounty','You received new bounty from '+user.name+' for the report '+bounty.report.title+'.Go and check it out.','L','I','/inbox?report='+bounty.report.id)
            # render success page on successful caputre of payment
            return redirect('https://app.cyber3ra.com/inbox?report='+str(bounty.report.id))
            return Response({"message": "Payment Successful","show": True,"paid": True,"report": bounty.report.id})
        except Exception as e:

            # print('not captured',e)
            newcomment = Comment(report=bounty.report, posted_by=user, type='Rc',body=bounty.amount)
            newcomment.save()
            # if there is an error while capturing payment.
            return redirect('https://app.cyber3ra.com/inbox?report='+str(bounty.report.id))
            return Response({"message": "Something went wrong with Payment","error": True,"paid": False,"report": bounty.report.id})
    except:
        # print('signature errior')
        newcomment = Comment(report=bounty.report, posted_by=user, type='Rc',body=bounty.amount)
        newcomment.save()
        # if signature verification fails.
        return redirect('https://app.cyber3ra.com/inbox?report='+str(bounty.report.id))
        return Response({"message": "Payment Unsuccessful, Signature Error","error": True,"paid": False,"report": bounty.report.id})
    # except:

    #     # if we don't find the required parameters in POST data
    #     return HttpResponseBadRequest()

    



    

@api_view(['GET'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsUser])
def bounty(request, id):
    user = User.objects.get(id=request.user.id)
    bount = Bounty.objects.get(id=id)
    if user != bount.to:
        return Response({"error": "True","message": "Error trying to claim"})
    days = timezone.now() - bount.date 
    # if days.days < 1:
    #     return Response({"error": "True","message": "Bounty can be claimed after 2 days"})
    try:
        user.account
    except ObjectDoesNotExist:
        return Response({"error": "True","message": "You need to add Fund account to claim bounty"})
    bount.requested = True
    bount.reqdate = timezone.now()
    bount.save()
    # return Response(SelfProfilingSerializer(bount.to, many=False, context={'request': request}).data)
    return Response({"details": SelfProfilingSerializer(user, many=False, context={'request': request}).data,"show": True,"message": "Claiming Request Successfully Sent"})
    return Response({"error": "True","message": "Error trying to claim3"})





    

@api_view(['POST'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsUser])
def funding(request):
    user = User.objects.get(id=request.user.id)
    if len(request.data['name']) < 1:
        return Response({"error": True,"message": "Please add details properly"})
    if request.data['mode'] == 0:
        print('upi')
        if len(request.data['upi']) < 1 or not re.match(r"[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}", request.data['upi']):
            return Response({"error": True,"message": "Please add details properly"})
        print('')
        try:
            user.account
            return Response({"error": True,"message": "You already have an account attached"})
        except ObjectDoesNotExist:
            # try:
                account = FundAccount(type='vpa', upi=request.data['upi'], user=user,name=request.data['name'])
                account.save()
                return Response({"details": SelfProfilingSerializer(user, many=False, context={'request': request}).data,"show": True,"message": "Fund Account Added Successfully"})
            # except Exception as e:
            #     print(e)
            #     return Response({"error": True,"message": "Error Trying to Add Account"})
    elif request.data['mode'] == 1:
        print('bank')
        if len(request.data['account']) < 1 or len(request.data['ifsc']) < 1 :
            return Response({"error": True,"message": "Please add details properly"})
    else:
        return Response({"error": True,"message": "Error Trying to Add Account"})
    print(request.data)
    # if not ['']:
    #     return Response({"error": "True","message": "Error trying to claim"})
    # days = timezone.now() - bount.date 
    # if days.days < 1:
    #     return Response({"error": "True","message": "Bounty can be claimed after 2 days"})
    # try:
    #     user.account
    # except ObjectDoesNotExist:
    #     return Response({"error": "True","message": "You need to add Fund account to claim bounty"})
    # bount.requested = True
    # bount.reqdate = timezone.now()
    # bount.save()
    # return Response(SelfProfilingSerializer(bount.to, many=False, context={'request': request}).data)
    return Response({"error": "True","message": "Error trying to claim3"})




    # claim = razorpay_client.payment_link.create(dict(amount=int(float(request.data['amount'])*100),currency='INR',))
    # claim = razorpay_client.payment.transfer(dict(amount=int(float(request.data['amount'])*100),currency='INR', payment_capture='0'))
    # post_data = {'name': 'Gladys'}

    # session = requests.Session()
    # session.auth = (settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET)
    # data = {
    #     "account_number": "2323230078386402", "amount": int(float(request.data['amount'])*100), "currency": "INR", "mode": "UPI", "purpose": "refund",
    #     "fund_account": {
    #         "account_type": "vpa",
    #         "vpa": {
    #             "address": request.data["upi"]
    #         },
    #         "contact": {
    #             "name": user.name,
    #             "email": user.email,
    #             "contact": user.contact,
    #             "type": "self",
    #         }
    #     },
    #     "queue_if_low_balance": False,
    # }
    # response = session.post('https://api.razorpay.com/v1/payouts', 
    # data=data, 
    # headers={'Authorization': 'Basic xqJZSv1pzB2IM5I862aD02fJ'})
    # content = response.content
    # print(content)
    # print(request.data)

    

@api_view(['POST'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsUser])
def checkemail(request):
    try:
        User.objects.get(email=request.data["email"])
        return Response({"error" : True, "message": "Entered Email is already in use"})
    except:
        return Response({"show" : True, "message": "Entered Email is available"})
    

@api_view(['POST'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsUser])
def changeemail(request):
    try:
        User.objects.get(email=request.data["email"])
        return Response({"error" : True, "message": "Entered Email is already in use"})
    except:
        user = User.objects.get(id=request.user.id)
        if user.check_password(request.data["password"]):
            user.email = request.data["email"]
            user.save()
            return Response({"show" : True, "message": "Email Successfully Changed"})
        else:
            return Response({"error" : True, "message": "Entered Password is Incorrect"})



@api_view(['POST'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsUser])
def checkusername(request):
    try:
        User.objects.get(username__iexact=request.data["username"])
        return Response({"error" : True, "message": "Entered Username is already in use"})
    except:
        return Response({"show" : True, "message": "Entered Email is available"})
    

@api_view(['POST'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsUser])
def changeusername(request):
    try:
        User.objects.get(username__iexact=request.data["username"])
        return Response({"error" : True, "message": "Entered Username is already in use"})
    except:
        user = User.objects.get(id=request.user.id)
        if user.check_password(request.data["password"]):
            user.username = request.data["username"]
            user.save()
            return Response({"show" : True, "message": "Username Successfully Changed"})
        else:
            return Response({"error" : True, "message": "Entered Password is Incorrect"})



