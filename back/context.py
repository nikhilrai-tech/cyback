from django.db.models.functions.datetime import ExtractMonth

from other.models import Notification
from .models import User
from main.models import Program, Report
import json
from datetime import timedelta
from django.db.models import Count, Sum
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.functions import TruncMonth
from django.apps import apps




def chart_context(request):
    # print(request.path)
    extra_context = {}
    # print(apps.get_app_configs())
    if request.path in ['/panel/sendemail','/panel/sendemail/']:
      #  print('entered')
        extra_context['app_list'] = ['hi']
    # for app in apps.get_app_configs():
    #   #  print(app.models)
    if request.user.is_authenticated:
        if request.path=='/panel/':
            # three = timezone.now() - timedelta(days=91)
            # one = timezone.now() - timedelta(days=30)
            five = timezone.now() - timedelta(days=150)
            # eight = timezone.now() - timedelta(days=250)
            # extra_context["newusers"] = User.objects.filter(date_joined__gte=one).order_by('-date_joined')[:10] # for table
            # serializer = NewUsers(,many=True)

            newusers = (
                User.objects.filter(date_joined__gte=five).annotate(date=TruncMonth('date_joined')).values('date').annotate(y=Count('id')).values('date' , 'y').order_by('date')
            )
            newus = json.dumps(list(newusers), cls=DjangoJSONEncoder)

            newprograms = (
                Program.objects.filter(published__gte=five).annotate(date=TruncMonth('published')).values('date').annotate(y=Count('id')).values('date' , 'y').order_by('date')
            )
            newprog = json.dumps(list(newprograms), cls=DjangoJSONEncoder)

            extra_context["newusers"] = newus # for chart
            extra_context["newprograms"] = newprog # for chart
            # tots = User.objects.aggregate(Sum('totalreputation'))['totalreputation__sum']
            # User.objects.values('totalreputation').annotate(total_reputation=Count('totalreputation'))
            # print(tots)
            extra_context["total_reputation"] = User.objects.aggregate(Sum('totalreputation'))['totalreputation__sum']
            extra_context["users_count"] = User.objects.count() # Lengths
            extra_context["report_count"] = Report.objects.count() # Lengths
            extra_context["program_count"] = Program.objects.count() # Lengths
            extra_context["new_users_all"] = User.objects.filter(type__in=['U','Ct','A']).order_by('-date_joined')[:5]
            extra_context["new_companies_all"] = User.objects.filter(type='C').order_by('-date_joined')[:5]
            extra_context["rep_users"] = User.objects.filter(is_staff=False,is_superadmin=False,is_admin=False).order_by('-totalreputation')[:5]
            # extra_context['app_list'] = get_app_list
            # extra_context["lengths"] = {
            #     'wcons': len(wcons),
            #     'fcons': len(fcons),
            #     'fbids': len(fbids),
            #     'wbids': len(wbids),
            #     'wnego': len(wnego),
            #     'fnego': len(fnego),
            #     'pays': len(pays),
            # } # for chart
        extra_context["notis"] = Notification.objects.filter(of=request.user).order_by('-pdate')
    return extra_context
