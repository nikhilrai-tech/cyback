from multiprocessing import context
from urllib import request
from rest_framework import serializers
from django.db.models.query_utils import Q
from.models import *
from django.contrib.auth.models import auth
from django.contrib.admin.models import LogEntry

from django.contrib.auth import get_user_model
from main.models import Program, Report, Thanks, Scope
from other.models import Bounty
from django.utils.timesince import timesince
import json
from django.core.exceptions import ObjectDoesNotExist
from datetime import timedelta
from django.db.models import Count, Sum
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.functions import TruncMonth
from django.utils import timezone
# from django.utils.timezone import utc
from pytz import timezone as tz
# import tzlocal


class UserSerializer(serializers.ModelSerializer):
	def create(self, validated_data):
		return get_user_model().objects.create_user(**validated_data)
	profile = serializers.SerializerMethodField('get_image_url')
	# award = serializers.SerializerMethodField('get_award')
	# def get_award(self, obj):
	# 	return sorted(obj.get_award_length(request=self.context['request'])[-3:])
	def get_image_url(self, obj):
		request = self.context.get('request')
		return request.build_absolute_uri(obj.photo.url) if obj.photo else None
	class Meta:
		model = get_user_model()
		fields = ('email', 'password', 'name', 'totalreputation','username','is_staff','is_company','profile')
		extra_kwargs = {
			'password': {'write_only': True, 'min_length': 8},
		}














































class UserDashSerializer(serializers.ModelSerializer):
	count = serializers.SerializerMethodField('get_counts')
	awards = serializers.SerializerMethodField('get_awards')
	report_overview = serializers.SerializerMethodField('get_report_overview')
	def get_awards(self, obj):
		arr = obj.get_award_length(request=self.context['request'])
		return {"earned": len(arr),"indexes": sorted(arr[-3:])}
	def get_report_overview(self, obj):
		five = timezone.now() - timedelta(days=150)
		newreports = (
			Report.objects.filter(published__gte=five, posted_by=User.objects.get(id=obj.id)).annotate(date=TruncMonth('published')).values('date').annotate(y=Count('id')).values('date' , 'y').order_by('date')
		)
		return list(newreports)
	def get_counts(self, obj):
		return {
			"referred": obj.refreputation, "visits": obj.visits, "reputation": obj.totalreputation, "likes": len(obj.likes.all()),
			"bounties" : sum(list(Bounty.objects.filter(to=obj).values_list("amount", flat=True)))
		}
	class Meta:
		model = get_user_model()
		fields = ('count' ,'awards','report_overview')
		

class CompanyDashSerializer(serializers.ModelSerializer):
	count = serializers.SerializerMethodField('get_counts')
	overview = serializers.SerializerMethodField('get_overview')
	staff = serializers.SerializerMethodField('get_staff')
	programs = serializers.SerializerMethodField('get_programs')
	def get_overview(self, obj):
		user = User.objects.get(id=obj.id)
		programs = Program.objects.filter(posted_by=user)
		five = timezone.now() - timedelta(days=150)
		newprograms = (
			Program.objects.filter(published__gte=five, posted_by=user).annotate(date=TruncMonth('published')).values('date').annotate(y=Count('id')).values('date' , 'y').order_by('date')
		)
		newreports = (
			Report.objects.filter(published__gte=five, program__in=programs).annotate(date=TruncMonth('published')).values('date').annotate(y=Count('id')).values('date' , 'y').order_by('date')
		)
		return {"reports": list(newreports),"programs": list(newprograms)}
	def get_programs(self, obj):
		user = User.objects.get(id=obj.id)
		progs = Program.objects.filter(posted_by=user).order_by('-published')[:5]
		return ProgramSerializerShort(progs,many=True).data
	def get_staff(self, obj):
		user = User.objects.get(id=obj.id)
		newusers = User.objects.filter(refuser=user).order_by('-date_joined')[:5]
		return BaseSerializer2(newusers,many=True).data
	def get_counts(self, obj):
		user = User.objects.get(id=obj.id)
		programs = Program.objects.filter(posted_by=user)
		res = 0
		for pro in programs:
			res += pro.resolved
		return {
			"referred": len(User.objects.filter(refuser=user)), "visits": obj.visits, "reports": Report.objects.filter(program__in=programs).count(), "programs": programs.count(), "resolved": res,
			"closed": Report.objects.filter(program__in=programs,status__in=['C','R','B','N','A','D']).count(),"pending":Report.objects.filter(program__in=programs,status__in=['P']).count(),
			"inscope": Scope.objects.filter(company=user,out=False).count(),"outscope": Scope.objects.filter(company=user,out=True).count(),
			"bounty" : sum(list(Bounty.objects.filter(fro=obj).values_list("amount", flat=True)))
		}
	class Meta:
		model = get_user_model()
		fields = ('count' ,'overview','staff','programs')

class StaffDashSerializer(serializers.ModelSerializer):
	count = serializers.SerializerMethodField('get_counts')
	overview = serializers.SerializerMethodField('get_overview')
	staff = serializers.SerializerMethodField('get_staff')
	programs = serializers.SerializerMethodField('get_programs')
	def get_overview(self, obj):
		user = User.objects.get(id=obj.id)
		programs = Program.objects.filter(posted_by=user.refuser)
		five = timezone.now() - timedelta(days=150)
		newprograms = (
			Program.objects.filter(published__gte=five, posted_by=user.refuser).annotate(date=TruncMonth('published')).values('date').annotate(y=Count('id')).values('date' , 'y').order_by('date')
		)
		newreports = (
			Report.objects.filter(published__gte=five, program__in=programs).annotate(date=TruncMonth('published')).values('date').annotate(y=Count('id')).values('date' , 'y').order_by('date')
		)
		return {"reports": list(newreports),"programs": list(newprograms)}
	def get_programs(self, obj):
		user = User.objects.get(id=obj.id)
		progs = Program.objects.filter(posted_by=user.refuser).order_by('-published')[:5]
		return ProgramSerializerShort(progs,many=True).data
	def get_staff(self, obj):
		user = User.objects.get(id=obj.id)
		newusers = User.objects.filter(refuser=user.refuser).order_by('-date_joined')[:5]
		return BaseSerializer2(newusers,many=True).data
	def get_counts(self, obj):
		user = User.objects.get(id=obj.id)
		programs = Program.objects.filter(posted_by=user.refuser)
		res = 0
		for pro in programs:
			res += pro.resolved
		return {
			"referred": 0, "visits": obj.visits, "reports": Report.objects.filter(program__in=programs).count(), "programs": programs.count(), "resolved": res,
			"closed": Report.objects.filter(program__in=programs,status__in=['C','R','B','N','A','D']).count(),"pending":Report.objects.filter(program__in=programs,status__in=['P']).count(),
			"inscope": Scope.objects.filter(company=user.refuser,out=False).count(),"outscope": Scope.objects.filter(company=user.refuser,out=True).count(),
			"bounty" : sum(list(Bounty.objects.filter(fro=obj).values_list("amount", flat=True)))
		}
	class Meta:
		model = get_user_model()
		fields = ('count' ,'overview','staff','programs')















































class BaseSerializer(serializers.ModelSerializer):
	class Meta:
		model=User
		fields=(
			'username' ,'photo','name'
		)
		depth=1

class BaseSerializer2(serializers.ModelSerializer):
	joined = serializers.SerializerMethodField('get_join')
	def get_join(self, obj):
		return timesince(obj.date_joined)
	class Meta:
		model=User
		fields=(
			'username' ,'photo','name','joined'
		)
		depth=1
		

#working
class BaseCompanySerializer(serializers.ModelSerializer):
	class Meta:
		model=User
		fields=(
			'bio' ,'photo','name','username'
		)
		depth=1
		







class ProgramSerializerShort(serializers.ModelSerializer):
	type = serializers.CharField(source='get_type_display')
	class Meta:
		model=Program
		# ,'efficiency'
		fields=(
			'type','title'
		)
		depth=2
class ProgramSerializer(serializers.ModelSerializer):
	type = serializers.CharField(source='get_type_display')
	class Meta:
		model=Program
		# ,'efficiency'
		fields=(
			'active','criticreward','lowreward','managed','splitting','type','updated','title'
		)
		depth=2


class ReportSerializerShort(serializers.ModelSerializer):
	# severity = serializers.CharField(source='get_severity_display')
	photo = serializers.SerializerMethodField('photo_method')
	user = serializers.SerializerMethodField('user_method')
	posted = serializers.SerializerMethodField('posted_method')
	def photo_method(self,obj):
		user =  self.context['request'].user
		userd = User.objects.get(id=user.id)
		if userd.type == 'U':
			return obj.program.posted_by.photo.url if obj.program.posted_by.photo else None
		else:
			return obj.posted_by.photo.url if obj.posted_by.photo else None
	def user_method(self,obj):
		user =  self.context['request'].user
		userd = User.objects.get(id=user.id)
		if userd.type == 'U':
			return obj.program.posted_by.name if obj.program.posted_by.name else obj.program.posted_by.username
		else:
			return obj.posted_by.name if obj.posted_by.name else obj.posted_by.username
	def posted_method(self,obj):
		return timesince(obj.published)
	class Meta:
		model=Report
		# ,'efficiency'
		fields=('photo','title','user','id','posted'
		)
		depth=2







class ThanksSerializer(serializers.ModelSerializer):
	fro = BaseCompanySerializer(many=False)
	to = BaseSerializer(many=False)
	class Meta:
		model=Thanks
		# ,'efficiency'
		fields=(
			'fro','to','reputation','date'
		)
		depth=1


class BountySerializer(serializers.ModelSerializer):
	# fro = BaseCompanySerializer(many=False)
	# to = BaseSerializer(many=False)
	report = ReportSerializerShort(many=False)
	user = serializers.SerializerMethodField('other_user')
	status = serializers.SerializerMethodField('get_status')
	def other_user(self, obj):
		user = self.context['request'].user
		userd = User.objects.get(id=user.id)
		if userd.type=='C' or userd.type=='Ct':
			return BaseSerializer(obj.to, many=False).data
		elif userd.type=='U':
			return BaseCompanySerializer(obj.fro, many=False).data
		else:
			return {"error": True,"message": "Admin not Allowed"} 
	def get_status(self, obj):
		print(obj.claimed, obj.requested, obj.paid)
		if obj.claimed:
			return 'Claimed'
		elif not obj.claimed and obj.requested:
			return 'Requested'
		elif not obj.claimed and not obj.requested and not obj.paid:
			return 'Invalid Bounty'
		else: 
			return 'To be Claimed'
	class Meta:
		model=Bounty
		# ,'efficiency'
		fields=(
			'user','date','report','amount','status','id'
		)
		depth=1



















































#working
class ProfilingSerializer(serializers.ModelSerializer):
	liked = serializers.SerializerMethodField('is_liked')
	atype = serializers.CharField(source='get_type_display')
	error = serializers.SerializerMethodField('is_error')
	likes = serializers.SerializerMethodField('likescount')
	reports = serializers.SerializerMethodField('reportscount')
	awards = serializers.SerializerMethodField('awardscount')
	hactivity = serializers.SerializerMethodField('reportsall')
	thanks = serializers.SerializerMethodField('thanksall')
	def is_liked(self, obj):
		user =  self.context['request'].user
		# print(user.id)
		# print(obj.get_award_length(request=self.context['request']))
		if User.objects.get(id=user.id) in obj.likes.all():
			return True
		else:
			return False
	def is_error(self, obj):
		return False
	def likescount(self, obj):
		return len(obj.likes.all())
	def reportscount(self, obj):
		return Report.objects.filter(posted_by=User.objects.get(id=obj.id)).count()
	def awardscount(self, obj):
		return obj.get_award_length(request=self.context['request'])
	def reportsall(self, obj):
		return []
		# user =  self.context['request'].user
		return  ReportSerializerShort(Report.objects.filter(posted_by=User.objects.get(id=obj.id)), many=True, context={'request': self.context['request']}).data 
	def thanksall(self, obj):
		return []
		# here
		# user =  self.context['request'].user
		thankss = Thanks.objects.filter(to=User.objects.get(id=obj.id))
		return ThanksSerializer(thankss, many=True, context=self.context).data
	class Meta:
		model=User
		fields=(
			'error','username','atype' ,'photo','name','bio' ,'totalreputation','upvotereputation','verificationreputation','likesreputation','otherreputation',
			'refreputation','liked','likes','reports','visits','email_confirmed','hactivity','thanks','github','facebook','twitter','instagram','website','awards'
		)
		depth=2



		




#User self Profile
class SelfProfilingSerializer(serializers.ModelSerializer):
	atype = serializers.CharField(source='get_type_display')
	error = serializers.SerializerMethodField('is_error')
	likesc = serializers.SerializerMethodField('likescount')
	reports = serializers.SerializerMethodField('reportscount')
	awards = serializers.SerializerMethodField('awardscount')
	hactivity = serializers.SerializerMethodField('reportsall')
	thanks = serializers.SerializerMethodField('thanksall')
	bounties = serializers.SerializerMethodField('bountiesall')
	# likes = BaseSerializer(many=True, max_length=3)
	likes = serializers.SerializerMethodField('likeslist')
	fund_account = serializers.SerializerMethodField('funding')
	
	def funding(self, obj):
		try:
			return {"type": obj.account.get_type_display(),"primary": obj.account.upi if obj.account.type == 'vpa' else obj.account.accountno,"name": obj.account.name}
		except ObjectDoesNotExist:
			return False
	
	def likeslist(self, obj):
		qs = obj.likes.all()
		if not 'verbose' in self.context:
			qs = qs[:3]
		return BaseSerializer(qs, many=True, context={'request': self.context['request']}).data

	def is_liked(self, obj):
		user =  self.context['request'].user
		# print(user.id)
		# print(obj.get_award_length(request=self.context['request']))
		if User.objects.get(id=user.id) in obj.likes.all():
			return True
		else:
			return False
	def is_error(self, obj):
		return False
	def likescount(self, obj):
		return len(obj.likes.all())
	def reportscount(self, obj):
		user =  self.context['request'].user
		return Report.objects.filter(posted_by=User.objects.get(id=user.id)).count()
	def awardscount(self, obj):
		return sorted(obj.get_award_length(request=self.context['request'])[-3:])[::-1]
	def reportsall(self, obj):
		user =  self.context['request'].user
		userd = User.objects.get(id=user.id)
		if userd.type == 'C':
			progs = Program.objects.filter(posted_by=userd)
			return ProgramSerializer(progs, many=True).data
		if userd.type == 'Ct':
			progs = Program.objects.filter(posted_by=userd.refuser)
			return ProgramSerializer(progs, many=True).data
		elif userd.type == 'U':
			return ReportSerializerShort(Report.objects.filter(posted_by=userd), many=True, context={'request': self.context['request']}).data 
		else:
			return []
	def thanksall(self, obj):
		user =  self.context['request'].user
		thankss = Thanks.objects.filter(to=User.objects.get(id=user.id)).order_by('-date')
		return ThanksSerializer(thankss, many=True,context=self.context).data
	def bountiesall(self, obj):
		user =  self.context['request'].user
		bounties = Bounty.objects.filter(to=User.objects.get(id=user.id)).order_by('-date')
		return BountySerializer(bounties, many=True,context=self.context).data
	class Meta:
		model=User
		fields=(
			'error','username','email','atype' ,'photo','name','bio' ,'totalreputation','upvotereputation','verificationreputation','likesreputation','otherreputation','refcode',
			'refreputation','likes','likesc','reports','visits','email_confirmed','hactivity','thanks','github','facebook','twitter','instagram','website','linkedin','awards','bounties','fund_account'
		)
		depth=2


#Company Profile
class CompanyProfilingSerializer(serializers.ModelSerializer):
	atype = serializers.CharField(source='get_type_display')
	refreputation = serializers.SerializerMethodField('staff')
	error = serializers.SerializerMethodField('is_error')
	likesc = serializers.SerializerMethodField('likescount')
	reports = serializers.SerializerMethodField('reportscount')
	awards = serializers.SerializerMethodField('awardscount')
	hactivity = serializers.SerializerMethodField('reportsall')
	thanks = serializers.SerializerMethodField('thanksall')
	bounties = serializers.SerializerMethodField('bountiesall')
	def is_liked(self, obj):
		user =  self.context['request'].user
		# print(user.id)
		# print(obj.get_award_length(request=self.context['request']))
		if User.objects.get(id=user.id) in obj.likes.all():
			return True
		else:
			return False
	def is_error(self, obj):
		return False
	def staff(self, obj):
		return len(User.objects.filter(refuser__in=[User.objects.get(id=self.context['request'].user.id)]))
	def likescount(self, obj):
		return len(obj.likes.all())
	def reportscount(self, obj):
		user =  self.context['request'].user
		return Report.objects.filter(posted_by=User.objects.get(id=user.id)).count()
	def awardscount(self, obj):
		return obj.get_award_length(request=self.context['request'])
	def reportsall(self, obj):
		user =  self.context['request'].user
		userd = User.objects.get(id=user.id)
		if userd.type == 'C':
			progs = Program.objects.filter(posted_by=userd)
			return ProgramSerializer(progs, many=True, context=self.context).data
		if userd.type == 'Ct':
			progs = Program.objects.filter(posted_by=userd.refuser)
			return ProgramSerializer(progs, many=True, context=self.context).data
		elif userd.type == 'U':
			reps = Report.objects.filter(posted_by=userd)
			return ReportSerializerShort(reps, many=True, context={'request': self.context['request']}).data 
		else:
			return []
	def thanksall(self, obj):
		user =  self.context['request'].user
		thankss = Thanks.objects.filter(fro=User.objects.get(id=user.id))
		return ThanksSerializer(thankss, many=True, context=self.context).data
	def bountiesall(self, obj):
		user =  self.context['request'].user
		bounties = Bounty.objects.filter(fro=User.objects.get(id=user.id)).order_by('-date')
		return BountySerializer(bounties, many=True,context=self.context).data
	class Meta:
		model=User
		fields=(
			'error','username','email','likes','atype' ,'photo','name','bio' ,'refreputation','likesc','reports','visits','email_confirmed','hactivity','thanks','github','facebook','twitter','instagram','website','awards','bounties'
		)
		depth=2



		























































#working
class StaffSerializer(serializers.ModelSerializer):
	freezed = serializers.SerializerMethodField('is_freezed')
	verified = serializers.SerializerMethodField('is_verified')
	def is_freezed(self,obj):
		return not obj.is_active
	def is_verified(self,obj):
		return obj.email_confirmed
	class Meta:
		model=User
		fields=(
			'username' ,'email','photo','name','bio' ,'freezed','verified'
		)
		depth=1
# ,'totalreputation'

#working
class ProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model=User
		fields=(
			'username' ,'photo','name','bio' ,'totalreputation','upvotereputation','refreputation'
		)
		depth=1
		
class ProfileSerializerPrivate(serializers.ModelSerializer):
	class Meta:
		model=User
		fields=(
			'username' ,'totalreputation'
		)
		depth=1
