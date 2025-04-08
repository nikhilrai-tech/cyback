from django.db import models

# Create your models here.
from django.core.validators import MaxValueValidator, MinValueValidator
from random import randint 


def random_report_id():
    n = randint(10000000, 99999999)
    try :
        user = Report.objects.get(id=n)
        return random_report_id()
    except:
        return n


class Program(models.Model):
    TYPE_CHOICES = (
        ('BBP', 'Bug Bounty Program'),
        ('VDP', 'Vulnerability Disclosure Program'),
        ('PRI', 'Private Program'),
    )
    title = models.CharField(max_length=100, verbose_name='Program Title', unique=True)
    type = models.CharField(max_length=100, choices=TYPE_CHOICES, verbose_name='Program Type')
    policy = models.CharField(max_length=500, blank=True, null=True, verbose_name='Program Policy')
    resolved = models.IntegerField(default=0, verbose_name='Reports Resolved')
    lowreward = models.IntegerField(default=0, verbose_name='Low Reward in ₹')
    midreward = models.IntegerField(default=0, verbose_name='Medium Reward in ₹')
    highreward = models.IntegerField(default=0, verbose_name='High Reward in ₹')
    criticreward = models.IntegerField(default=0, verbose_name='Critical Reward in ₹')
    active = models.BooleanField(default=False, verbose_name='Active')
    managed = models.BooleanField(default=False, verbose_name='Managed By Cyber3ra')
    updated = models.BooleanField(default=False, verbose_name='Updated')
    splitting = models.BooleanField(default=False, verbose_name='Bounty Splitting Eligible')
    efficiency = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(1)])
    posted_by = models.ForeignKey('back.User', blank=True, null=True, related_name='program_posted_by', verbose_name='Posted By Company', on_delete=models.CASCADE)
    subscribed = models.ManyToManyField('back.User', blank=True, related_name='Users_subscribing_this_program', verbose_name='Users Invited to this Program')
    thanks = models.ManyToManyField('main.Thanks', blank=True, related_name='Users_thanked_for_this_program', verbose_name='Thanked Users')
    scopes = models.ManyToManyField('main.Scope', blank=True, related_name='scopes_related', verbose_name='Scopes')
    published = models.DateTimeField(auto_now_add=True, verbose_name='Date Posted')
    lastedited = models.DateTimeField(auto_now=True, verbose_name='Last Edited')
    background = models.ImageField(upload_to='programs', blank=True, null=True, verbose_name='Background Image')
    deleted = models.BooleanField(default=False, verbose_name='Deleted')
    external = models.CharField( max_length=500, blank=True, null=True,verbose_name='Managed By External')  # Add this line

    def save(self, *args, **kwargs):
        super(Program, self).save(*args, **kwargs)

    def __str__(self):
        return self.title + ' | ' + self.get_type_display()
		#  + ' | '+ (self.posted_by.name if self.posted_by.name else self.posted_by.username)


class Scope(models.Model):
	SCOPE_CHOICES = (
		('C','Critical'),
		('H','High'),
		('M','Medium'),
		('L','Low'),
		('N','None'),
	)
	MAIN_CHOICES = (
		('1','CIDR'),
		('2','Domain'),
		('3','iOS: App Store'),
		('4','iOS: Testflight'),
		('5','iOS: .ipa'),
		('6','Android: Play Store'),
		('7','Android: .apk'),
		('8','Windows: Microsoft Store'),
		('9','Source Code'),
		('10','Executable'),
		('11','Hardware/IoT'),
		('12','Other'),
	)
	type = models.CharField(max_length=100, choices=MAIN_CHOICES,verbose_name='Scope Type')
	domain = models.CharField(max_length=100,verbose_name='Domain/Environment')
	markdown = models.TextField(max_length=400, blank=True, null=True,verbose_name='Description')
	tags = models.CharField(max_length=400, default='',verbose_name='Tags')
	severity = models.CharField(max_length=100, choices=SCOPE_CHOICES,default='M',verbose_name='Severity')
	bounty = models.BooleanField(default=False,verbose_name='Bounty Eligible')
	out = models.BooleanField(default=False,verbose_name='Out of Scope')
	company = models.ForeignKey('back.User',blank=True,null=True,on_delete=models.CASCADE)
	def __str__(self):
		return self.get_type_display() + '('+self.domain+')'







class Report(models.Model):
	SCOPE_CHOICES = (
		('C','Critical'),
		('H','High'),
		('M','Medium'),
		('L','Low'),
		('N','None'),
	)
	STATUS_CHOICES = (
		('P','In Progress'),
		('C','Completed'),
		('R','Rejected'),
		('B','Rewarded'),
		('N','Not Applicable'),
		('A','Accepted'),
		('D','Duplicate'),
	)
	id = models.IntegerField(primary_key=True, default=random_report_id, editable=False, unique=True)
	title = models.CharField(max_length=100, verbose_name='Title')
	status = models.CharField(max_length=100, choices=STATUS_CHOICES,default='P',verbose_name='Status')
	program = models.ForeignKey('main.Program',blank=True, related_name='program_selected',verbose_name='Program',on_delete=models.CASCADE)
	description = models.CharField(max_length=500,blank=True,null=True,verbose_name='Description')
	impact = models.CharField(max_length=500,blank=True,null=True,verbose_name='Impact')
	weakness = models.CharField(max_length=100, verbose_name='Weakness')
	severity = models.CharField(max_length=100, choices=SCOPE_CHOICES,default='M',verbose_name='Severity')
	disclosure = models.BooleanField(default=False,verbose_name='Public Disclosure')
	posted_by = models.ForeignKey('back.User',blank=True,null=True,related_name='report_posted_by',verbose_name='Posted By',on_delete=models.CASCADE)
	asset = models.ForeignKey('main.Scope',blank=True, related_name='scope_selected',verbose_name='Asset',on_delete=models.CASCADE)
	published = models.DateTimeField(auto_now_add=True,verbose_name='Date Posted')
	lastedited = models.DateTimeField(auto_now=True,verbose_name='Last Edited')
	disclosed = models.DateTimeField(null=True, blank=True,verbose_name='Date Disclosed')
	upvotes = models.ManyToManyField('back.User',blank=True, verbose_name='Upvotes',related_name='upvotes_by_user')
	photo0 = models.ImageField(upload_to='reports',blank=True,null=True,verbose_name='Report Attached File 1')
	photo1 = models.ImageField(upload_to='reports',blank=True,null=True,verbose_name='Report Attached File 2')
	photo2 = models.ImageField(upload_to='reports',blank=True,null=True,verbose_name='Report Attached File 3')
	deleted = models.BooleanField(default=False,verbose_name='Deleted')

	def save(self, *args, **kwargs):
		if self.status == 'A' or self.status == 'B':
			self.program.resolved += 1
			self.program.save()
		super(Report, self).save(*args, **kwargs)
	def __str__(self):
		return self.title





class Comment(models.Model):
	TYPE_CHOICES = (
		('A','Status Change'),
		('D','Request Disclosure'),
		('D2','Request Hide'),
		('T','Thanks'),
		('B','Body'),
		('Ri','Reward Initiated'),
		('Rs','Reward Success'),
		('Rc','Reward Cancelled'),
	)
	report = models.ForeignKey('main.Report', related_name='comment_of_report',verbose_name='Report',on_delete=models.CASCADE)
	posted_by = models.ForeignKey('back.User', related_name='comment_posted_by',verbose_name='Posted By',on_delete=models.CASCADE)
	body = models.CharField(blank=True,null=True,verbose_name='Comment Body',max_length=500)
	request = models.BooleanField(default=False,verbose_name='Description Type')
	type = models.CharField(max_length=100, choices=TYPE_CHOICES,default='B',verbose_name='Type')
	date = models.DateTimeField(auto_now_add=True,verbose_name='Date Earned')

	def __str__(self):
		return 'Report : '+self.report.title+', ID '+str(self.id)



class Thanks(models.Model):
	fro = models.ForeignKey('back.User',blank=True, related_name='from_company',verbose_name='From Company',on_delete=models.CASCADE)
	to = models.ForeignKey('back.User',blank=True,null=True,related_name='to_user',verbose_name='To User',on_delete=models.CASCADE)
	description = models.CharField(blank=True,null=True,verbose_name='Description',max_length=250)
	reputation = models.IntegerField(default=1,verbose_name='Reputation Earned')
	date = models.DateTimeField(auto_now_add=True,verbose_name='Date Earned')

	def __str__(self):
		return 'From '+self.fro.username+', To '+self.to.username




class Job(models.Model):
	JOB_CHOICES = (
		('C','Contract'),
		('F','Full Time'),
	)
	designation = models.CharField(max_length=100,verbose_name='Job Title/Deignation')
	description = models.CharField(max_length=500,blank=True,null=True,verbose_name='Job Description')
	type = models.CharField(max_length=100, choices=JOB_CHOICES,default='F',verbose_name='Job Type')
	link = models.CharField(max_length=100,verbose_name='Job Link')
	location = models.CharField(max_length=100,verbose_name='Job Location')
	posted_by = models.ForeignKey('back.User',blank=True,null=True,related_name='job_posted_by',verbose_name='Posted By',on_delete=models.CASCADE)
	remote = models.BooleanField(default=False,verbose_name='Remote Friendly')
	out = models.BooleanField(default=False,verbose_name='Out of Scope')
	published = models.DateTimeField(auto_now_add=True,verbose_name='Date Posted')
	lastedited = models.DateTimeField(auto_now=True,verbose_name='Last Edited')








