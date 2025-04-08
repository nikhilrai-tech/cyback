from django.utils.timesince import timesince
# from pytz import timezone
from rest_framework import serializers
from back.models import User

from back.serializers import BaseCompanySerializer, BaseSerializer
from.models import *
from django.utils import timezone
# from django.contrib.auth.models import auth

# from django.contrib.auth import get_user_model


#working
class JobSerializer(serializers.ModelSerializer):
	type = serializers.CharField(source='get_type_display')
	class Meta:
		model=Job
		fields=(
			'__all__'
		)
		depth=2


class ScopeSerializer(serializers.ModelSerializer):
	type = serializers.CharField(source='get_type_display')
	# severity = serializers.CharField(source='get_severity_display')
	class Meta:
		model=Scope
		fields=(
			'id','bounty','domain','out','severity','type'
		)
		depth=2

class ScopeSerializerShort(serializers.ModelSerializer):
	type = serializers.CharField(source='get_type_display')
	# severity = serializers.CharField(source='get_severity_display')
	class Meta:
		model=Scope
		fields=('domain','type'
		)
		depth=2
		
class ProgramSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_type_display')
    scopes = ScopeSerializer(many=True)
    posted_by = BaseSerializer(many=False)
    perm = serializers.SerializerMethodField('has_perm')

    external = serializers.CharField()  

    def has_perm(self, obj):
        user = self.context['request'].user
        if user.id:
            userd = User.objects.get(id=user.id)
            if userd.type == 'U':
                perm = False
                for ob in obj.subscribed.all():
                    if ob.id == user.id:
                        perm = True
                return perm
            else:
                if user.id == obj.posted_by.id or userd.refuser.id == obj.posted_by.id:
                    return True
                else:
                    return False
        else:
            return False

    class Meta:
        model = Program
        fields = (
            'active', 'criticreward', 'lastedited', 'lowreward', 'managed', 'posted_by', 'published', 'scopes',
            'splitting', 'type', 'updated', 'title', 'perm', 'external'
        )
        depth = 2

		
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

		
# class ProgramSerializerPublic(serializers.ModelSerializer):
# 	type = serializers.CharField(source='get_type_display')
# 	scopes = ScopeSerializer(many=True)
# 	posted_by = BaseCompanySerializer(many=False)
# 	thanks = ThanksSerializer(many=True)
# 	perm = serializers.SerializerMethodField('has_perm')
# 	def has_perm(self,obj):
# 		return False
# 	class Meta:
# 		model=Program
# 		# ,'efficiency'
# 		fields=(
# 			'active','criticreward','lastedited','lowreward','midreward','highreward','managed','posted_by','published','scopes','splitting','type','updated','title','thanks','policy','background','perm'
# 		)
# 		depth=2
		
		
class ProgramSerializerMore(serializers.ModelSerializer):
	type = serializers.CharField(source='get_type_display')
	scopes = ScopeSerializer(many=True)
	posted_by = BaseCompanySerializer(many=False)
	thanks = ThanksSerializer(many=True)
	perm = serializers.SerializerMethodField('has_perm')
	dperm = serializers.SerializerMethodField('has_dperm')
	def has_perm(self,obj):
		user =  self.context['request'].user
		print(user)
		if user.id:
			userd = User.objects.get(id=user.id)
			if userd.type == 'U':
				perm = False
				for ob in obj.subscribed.all():
					if ob.id == user.id:
						perm = True
				return perm
			else:
				if user.id == obj.posted_by.id or userd.refuser.id == obj.posted_by.id:
					return True
				else:
					return False
		else: return False
	def has_dperm(self,obj):
		user =  self.context['request'].user
		print(user)
		if user.id:
			if user.id == obj.posted_by.id:
				return True
			else:
				return False
		else: return False
	reports = serializers.SerializerMethodField('reports_length')
	def reports_length(self, obj):
		return Report.objects.filter(program=obj).count()
	resolved = serializers.SerializerMethodField('resolved_length')
	def resolved_length(self, obj):
		return Report.objects.filter(program=obj, status__in=['C','B','A']).count()
	class Meta:
		model=Program
		# ,'efficiency'
		fields=(
			'active','criticreward','lastedited','lowreward','external','midreward','highreward','managed','posted_by','published','scopes','splitting','type','updated','title','thanks','policy','background','perm','dperm','reports','resolved'
		)
		depth=2
		
class ProgramSerializerShort(serializers.ModelSerializer):
	type = serializers.CharField(source='get_type_display')
	posted_by = BaseCompanySerializer(many=False)
	class Meta:
		model=Program
		# ,'efficiency'
		fields=('posted_by','type','title'
		)
		depth=2
		
		
class ReportSerializerShort(serializers.ModelSerializer):
	severity = serializers.CharField(source='get_severity_display')
	# status = serializers.CharField(source='get_status_display')
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
			return {"name":obj.program.posted_by.name if obj.program.posted_by.name else obj.program.posted_by.username,"username": obj.program.posted_by.username}
		else:
			return {"name": obj.posted_by.name if obj.posted_by.name else obj.posted_by.username,"username": obj.posted_by.username}
	def posted_method(self,obj):
		# print()
		try:
			latestcom = Comment.objects.filter(report=Report.objects.get(id=obj.id)).latest('date').date
			date = timesince(latestcom)
		except Exception as e:
			print(e)
			date = timesince(obj.lastedited)
		return date
		return timesince(obj.lastedited)
	class Meta:
		model=Report
		# ,'efficiency'
		fields=('photo','title','user','id','posted','severity'
		)
		depth=2

		
class ReportSerializerLong(serializers.ModelSerializer):
	asset = ScopeSerializerShort(many=False)
	severity = serializers.CharField(source='get_severity_display')
	status = serializers.CharField(source='get_status_display')
	photo = serializers.SerializerMethodField('photo_method')
	user = serializers.SerializerMethodField('user_method')
	posted = serializers.SerializerMethodField('posted_method')
	edited = serializers.SerializerMethodField('edited_method')
	amount = serializers.SerializerMethodField('range_method')
	def range_method(self,obj):
		# print(obj.severity)
		# print(obj.program.highreward)
		amounts = {
			'C': obj.program.criticreward,
			'H': obj.program.highreward,
			'M': obj.program.midreward,
			'L': obj.program.lowreward,
			'N': obj.program.lowreward,
			
		}
		return {'range': [obj.program.criticreward, obj.program.highreward, obj.program.midreward, obj.program.lowreward], 'actual': amounts[obj.severity]}
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
			return {"name":obj.program.posted_by.name if obj.program.posted_by.name else obj.program.posted_by.username,"username": obj.program.posted_by.username}
		else:
			return {"name": obj.posted_by.name if obj.posted_by.name else obj.posted_by.username,"username": obj.posted_by.username}
	def posted_method(self,obj):
		return timesince(obj.published)
	def edited_method(self,obj):
		return timesince(obj.published)
	class Meta:
		model=Report
		# ,'efficiency'
		fields=('photo','severity','title','user','id','posted','status', 'description', 'impact', 'weakness', 'asset','edited','disclosure','amount'
		)
		depth=2



















class PublicReportSerializerShort(serializers.ModelSerializer):
	severity = serializers.CharField(source='get_severity_display')
	status = serializers.CharField(source='get_status_display')
	photo = serializers.SerializerMethodField('photo_method')
	user = serializers.SerializerMethodField('user_method')
	to = serializers.SerializerMethodField('to_method')
	posted = serializers.SerializerMethodField('posted_method')
	upvotes = serializers.SerializerMethodField('get_upvotes')
	upvoted = serializers.SerializerMethodField('get_upvoted')
	def get_upvotes(self,obj):
		users = list(obj.upvotes.all())
		userser = BaseSerializer(users[:5], many=True)
		return {"length": len(users),"users": userser.data, "left": len(users) - 5 if len(users) > 5 else False}
	def get_upvoted(self,obj):
		user =  self.context['request'].user
		return user in obj.upvotes.all() if user else False
	def photo_method(self,obj):
		# user =  self.context['request'].user
		# userd = User.objects.get(id=user.id)
		# if userd.type == 'U':
		# 	return obj.program.posted_by.photo.url if obj.program.posted_by.photo else None
		# else:
			return obj.posted_by.photo.url if obj.posted_by.photo else None
	def user_method(self,obj):
		# user =  self.context['request'].user
		# userd = User.objects.get(id=user.id)
		# if userd.type == 'U':
		# 	return {"name":obj.program.posted_by.name if obj.program.posted_by.name else obj.program.posted_by.username,"username": obj.program.posted_by.username}
		# else:
			return {"name": obj.posted_by.name if obj.posted_by.name else obj.posted_by.username,"username": obj.posted_by.username}
	def to_method(self,obj):
		# user =  self.context['request'].user
		# userd = User.objects.get(id=user.id)
		# if userd.type == 'U':
			return {"name":obj.program.posted_by.name if obj.program.posted_by.name else obj.program.posted_by.username,"username": obj.program.posted_by.username}
		# else:
			# return {"name": obj.posted_by.name if obj.posted_by.name else obj.posted_by.username,"username": obj.posted_by.username}
	def posted_method(self,obj):
		# print()
		try:
			latestcom = Comment.objects.filter(report=Report.objects.get(id=obj.id)).latest('date').date
			date = timesince(latestcom)
		except Exception as e:
			print(e)
			date = timesince(obj.lastedited)
		return date
		return timesince(obj.lastedited)
	class Meta:
		model=Report
		# ,'efficiency'
		fields=('photo','title','user','id','posted','upvotes','upvoted','severity','status','to'
		)
		depth=2










		
class PublicReportSerializerLong(serializers.ModelSerializer):
	asset = ScopeSerializerShort(many=False)
	severity = serializers.CharField(source='get_severity_display')
	status = serializers.CharField(source='get_status_display')
	photo = serializers.SerializerMethodField('photo_method')
	user = serializers.SerializerMethodField('user_method')
	posted = serializers.SerializerMethodField('posted_method')
	edited = serializers.SerializerMethodField('edited_method')
	amount = serializers.SerializerMethodField('range_method')
	def range_method(self,obj):
		# print(obj.severity)
		# print(obj.program.highreward)
		amounts = {
			'C': obj.program.criticreward,
			'H': obj.program.highreward,
			'M': obj.program.midreward,
			'L': obj.program.lowreward,
			'N': obj.program.lowreward,
			
		}
		return {'range': [obj.program.criticreward, obj.program.highreward, obj.program.midreward, obj.program.lowreward], 'actual': amounts[obj.severity]}
	def photo_method(self,obj):
		user =  self.context['request'].user
		if user.id:
			userd = User.objects.get(id=user.id)
			if userd.type == 'U':
				return obj.program.posted_by.photo.url if obj.program.posted_by.photo else None
			else:
				return obj.posted_by.photo.url if obj.posted_by.photo else None
		else:
			return obj.posted_by.photo.url if obj.posted_by.photo else None
	def user_method(self,obj):
		user =  self.context['request'].user
		if user.id:
			userd = User.objects.get(id=user.id)
			if userd.type == 'U':
				return {"name":obj.program.posted_by.name if obj.program.posted_by.name else obj.program.posted_by.username,"username": obj.program.posted_by.username}
			else:
				return {"name": obj.posted_by.name if obj.posted_by.name else obj.posted_by.username,"username": obj.posted_by.username}
		else:
			return {"name": obj.posted_by.name if obj.posted_by.name else obj.posted_by.username,"username": obj.posted_by.username}
	def posted_method(self,obj):
		return timesince(obj.published)
	def edited_method(self,obj):
		return timesince(obj.published)
	class Meta:
		model=Report
		# ,'efficiency'
		fields=('photo','severity','title','user','id','posted','status', 'description', 'impact', 'weakness', 'asset','edited','disclosure','amount'
		)
		depth=2


		

		





















		

		
class CommentSerializer(serializers.ModelSerializer):
	posted_by = BaseSerializer(many=False)
	class Meta:
		model=Comment
		# ,'efficiency'
		fields=('type','body','posted_by','date','request'
		)
		depth=2