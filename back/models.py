
from django.db import models
from random import randint
from datetime import datetime
from main.models import Report, Program, Thanks
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.
import random
import os
from honeb.settings import BASE_DIR, MEDIA_ROOT
from django.core.files.storage import FileSystemStorage

class MyFileStorage(FileSystemStorage):

    # This method is actually defined in Storage
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(MEDIA_ROOT, name))
        return name # simply returns the name passed

mfs = MyFileStorage()

def random_string():
    n = str(randint(100000, 999999))
    try :
        user = User.objects.get(refcode=n)
        return random_string()
    except:
        return n


class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, password=None,name=None, type='U',refuser=None,active=True, other=0):
		user = self.model(email=self.normalize_email(email),username=username,name=name,type=type,refuser=refuser,is_active=active, otherreputation=other)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(email=self.normalize_email(email), password=password, username=username, type='S')
# 		user = self.model(email=self.normalize_email(email),username=username,name=None,contact=None,type=type,is_staff = True,is_admin = True,is_superadmin = True)
# 		user.save(using=self._db)
		return user

		
class User(AbstractBaseUser):
	TYPES = (
	    ('S','Super Admin'),
	    ('A','Admin'),
	    ('C','Company'),
	    ('Ct','Company Staff'),
	    ('U','User'),
	)
	CTYPES = (
	    ('S','Start-Up'),
	    ('E','Enterprise'),
	    ('M','Managed'),
	)
	username 				= models.CharField(verbose_name='Username',max_length=30, unique=True) #  , primary_key=True
	email 					= models.EmailField(verbose_name="Email", max_length=60, unique=True)
	name 				    = models.CharField(verbose_name='Name',max_length=50,blank=True,null=True)
	date_joined				= models.DateTimeField(verbose_name='Date Joined', auto_now_add=True)
	last_login				= models.DateTimeField(verbose_name='Last Login', auto_now=True)
	bio 			    	= models.CharField(verbose_name='Bio/Slogan',max_length=500,null=True,blank=True)
	email_confirmed			= models.BooleanField(default=False,verbose_name='Email Verified')
	phone_confirmed			= models.BooleanField(default=False)
	is_active				= models.BooleanField(default=False,verbose_name='Active')
	is_staff		    	= models.BooleanField(default=False,verbose_name='Company Staff Permissions')
	is_company		    	= models.BooleanField(default=False,verbose_name='Company Permissions')
	is_admin		    	= models.BooleanField(default=False,verbose_name='Admin Permissions')
	is_superadmin		    = models.BooleanField(default=False,verbose_name='Super Admin Permissions')
	type                    = models.CharField(choices=TYPES,verbose_name='Account Type',default='U',max_length=12)
	photo 		    	    = models.ImageField(upload_to='profiles',verbose_name='Profile Photo', blank=True,null=True)
	contact                 = models.CharField(max_length=12,blank=True,verbose_name='Contact Info', null=True)
	companytype             = models.CharField(max_length=100,blank=True,verbose_name='Company Type',choices=CTYPES, null=True)
	refreputation           = models.IntegerField(default=0, verbose_name='Referral Code Reputation') #REFERRAL CODE REPUTATION
	upvotereputation        = models.IntegerField(default=0, verbose_name='Upvotes Reputation') #UPVOTES REPUTATION
	likesreputation         = models.IntegerField(default=0, verbose_name='Likes Reputation') #LIKES REPUTATION
	verificationreputation  = models.IntegerField(default=0, verbose_name='Verification Reputation') #VERIFICATION REPUTATION
	otherreputation			= models.IntegerField(default=0, verbose_name='Main Reputation') #OTHER REPUTATION
	totalreputation         = models.IntegerField(default=0, verbose_name='Total Reputation') #GRAND TOTAL REPUTATION
	refcode                 = models.CharField(max_length=6,default=random_string,verbose_name='Referral Code') #REFFERAL CODE
	refuser					= models.ForeignKey('self',null=True,blank=True, on_delete=models.CASCADE, verbose_name='Attached To')
	likes					= models.ManyToManyField('self',blank=True, verbose_name='Likes',related_name='likes_by_user')
	visits			        = models.IntegerField(default=0, verbose_name='Profile Visits') #PROFILE VISITS
	reset					= models.DateTimeField(verbose_name='Previous Reset Time', null=True, blank=True)
# 	reputations 			= models.JSONField(verbose_name='Reputation Overview',blank=True,null=True)
	website 			    = models.URLField(verbose_name='Website URL',max_length=60,blank=True,null=True)
	github					= models.URLField(verbose_name='Github Link',blank=True, null=True)
	instagram				= models.URLField(verbose_name='Instagram Link',blank=True, null=True)
	facebook				= models.URLField(verbose_name='Facebook Link',blank=True, null=True)
	twitter					= models.URLField(verbose_name='Twitter Link',blank=True, null=True)
	linkedin				= models.URLField(verbose_name='LinkedIn Link',blank=True, null=True)
	phone_confirmed			= models.BooleanField(default=False)

	USERNAME_FIELD = 'username'
	
	REQUIRED_FIELDS = ['email'] 
	
	objects = MyAccountManager()

	def __init__(self, *args, **kwargs) -> None:
		self.classname = 'users'
		super().__init__(*args, **kwargs)

	def __str__(self):
		return self.email

	# For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
		# print(perm)
		# print(self.is_superadmin)
		if perm in ['back.add_user','main.add_job','main.change_job','main.add_program','main.change_program','main.change_scope',
		'main.add_scope','main.add_report','back.change_user','main.change_report','other.change_bounty','other.add_bounty','other.delete_bounty',
		'other.change_fundaccount','other.add_fundaccount','other.delete_fundaccount','other.delete_notification']:
			return False
		if perm in ['back.change_user','back.view_user']:
			return self.is_admin #and self.email_confirmed
		return self.is_admin #and self.email_confirmed
		# and self.email_confirmed and self.phone_confirmed

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return self.is_admin
	
	def get_award_length(self, *args, **kwargs):
		aws = [0,1,2]
		user = User.objects.get(id=self.id)
		funcs = {
			19: len(self.likes.all()) >= 250,
			18: len(self.likes.all()) >= 200,
			17: len(self.likes.all()) >= 100,
			16: Report.objects.filter(posted_by=user, status='A').count() >= 5,
			15: Report.objects.filter(posted_by=user, program__in=Program.objects.filter(type='PRI')).count() >= 1,
			14: len(self.likes.all()) >= 25,
			13: Thanks.objects.filter(to=user).count() >= 5,
			12: User.objects.filter(refuser__in=[user]).count() >= 5,
			11: Report.objects.filter(posted_by=user, status='A').count() >= 1,
			10: Thanks.objects.filter(to=user).count() >= 1,
			9: self.upvotereputation >= 5,
			8: len(self.likes.all()) >= 5,
			7: User.objects.filter(refuser__in=[user]).count() >= 1,
			6: Report.objects.filter(posted_by=user).count() >= 1,
			5: self.upvotereputation >= 2,
			4: User.objects.filter(likes__in=[user]).count() >= 5,
			3: self.bio and self.photo and self.name
        }
		for i in range(19,2,-1):
			if funcs[i]:
				aws.append(i)
		return aws
		return sorted(aws[-3:])
	# def get_absolute_url(self):
	# 	return "/people/%i/" % self.id

	def save(self, *args, **kwargs):
		self.totalreputation = self.refreputation + self.upvotereputation + self.likesreputation + self.verificationreputation + self.otherreputation
		# print(self.type)
		self.is_staff = self.type in ['S','A', 'C', 'Ct']
		self.is_company = self.type in ['S','A', 'C']
		self.is_admin = self.type in ['S','A']
		self.is_superadmin = self.type in ['S']
		# if self.type == 'S':
		# 	self.is_superadmin = True
		# 	self.is_admin = True
		# 	self.is_company = True
		# 	self.is_staff = True
		# elif self.type == 'A':
		# 	self.is_superadmin = False
		# 	self.is_admin = True
		# 	self.is_company = True
		# 	self.is_staff = True
		# elif self.type == 'C':
		# 	self.is_superadmin = False
		# 	self.is_admin = False
		# 	self.is_company = True
		# 	self.is_staff = True
		# elif self.type == 'Ct':
		# 	self.is_superadmin = False
		# 	self.is_admin = False
		# 	self.is_company = False
		# 	self.is_staff = True
		# else:
		# 	self.is_superadmin = False
		# 	self.is_admin = False
		# 	self.is_company = False
		# 	self.is_staff = False
		if not self._state.adding:
			self.likesreputation = len(self.likes.all()) if self.username else 0
		super(User, self).save(*args, **kwargs)
