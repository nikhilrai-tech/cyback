from tabnanny import verbose
from django.db import models
from django.utils import formats
# from honeb.settings import get_use
from back.models import User
import requests
import json
from honeb.settings import TEST_RAZOR_KEY_ID, TEST_RAZOR_KEY_SECRET, RAZOR_KEY_ID, RAZOR_KEY_SECRET
# User = get_user_model()

# Create your models here.

class Notification(models.Model):
	NOTI_CHOICES = (
		('P', "mdi-gift"),
		('J', "mdi-briefcase"),
		('I', "mdi-email"),
		('R', "mdi-note-text"),
		('L', "mdi-poll"),
		('U', "mdi-account"),
		('O', "mdi-bell"),
	)
	NOTI_TYPES = (
		('I', 'Info'),
		('S', 'Success'),
		('W', 'Warning'),
		('E', 'Error'),
	)
	of = models.ForeignKey(User,null=True, on_delete=models.CASCADE,related_name="Self_noti_user",verbose_name='For User')
	title = models.CharField(max_length=50)
	body = models.CharField(max_length=400)
	user = models.CharField(max_length=200,blank=True,null=True)
	type = models.CharField(max_length=50,choices=NOTI_CHOICES,default='O',verbose_name='Related to')
	ntype = models.CharField(max_length=50,choices=NOTI_TYPES,default='I',verbose_name='Type')
	link = models.CharField(max_length=50,default='#')
	date = models.DateField(auto_now_add=True)
	time = models.TimeField(auto_now_add=True)
	pdate = models.DateTimeField(auto_now_add=True,verbose_name='Date Received')
	seen = models.BooleanField(default=False)
	def save(self, *args, **kwargs):
		super(Notification, self).save(*args, **kwargs)
	def __str__(self):
		return self.title + ' | '+self.of.name if self.of.name else self.of.username+' ('+str(formats.date_format(self.pdate, 'd M Y h:m' ))+')'




		



class Bounty(models.Model):
	fro = models.ForeignKey('back.User', related_name='bounty_from_company',verbose_name='From Company',on_delete=models.CASCADE)
	to = models.ForeignKey('back.User',related_name='bounty_to_user',verbose_name='To User',on_delete=models.CASCADE)
	report = models.ForeignKey('main.Report',related_name='bounty_of_report',verbose_name='Of Report',on_delete=models.CASCADE)
	description = models.CharField(blank=True,null=True,verbose_name='Order ID',max_length=250)
	amount = models.IntegerField(default=False,verbose_name='Bounty Earned')
	date = models.DateTimeField(auto_now_add=True,verbose_name='Date Earned')
	paid = models.BooleanField(default=False,verbose_name='Is Paid')
	requested = models.BooleanField(default=False,verbose_name='Requested')
	reqdate = models.DateTimeField(null=True, blank=True,verbose_name='Date Requested')
	claimed = models.BooleanField(default=False,verbose_name='Claimed')
	cldate = models.DateTimeField(null=True, blank=True,verbose_name='Date Claimed')
	geticon = 'plated'
	__icon__ = 'plated'
	def __str__(self):
		return 'From '+self.fro.username+', To '+self.to.username
	def icon():
		return 'ghjdn'
	class Meta:
		verbose_name_plural = 'Bounties'

	def save(self, *args, **kwargs):
		if self.paid:
			self.report.status = 'B'
			self.report.save()
		super(Bounty, self).save(*args, **kwargs)





class FundAccount(models.Model):
	user = models.OneToOneField('back.User', related_name='account',verbose_name='Fund Account of User',on_delete=models.CASCADE)
	type = models.CharField(blank=True,null=True,verbose_name='Account Type',choices=(('bank_account','Bank Account'),('vpa','UPI Address'),),max_length=12)
	name = models.CharField(blank=True,null=True,verbose_name='Account Name',max_length=100)
	upi = models.CharField(blank=True,null=True,verbose_name='UPI Address',max_length=100)
	accountno = models.CharField(blank=True,null=True,verbose_name='Account No',max_length=50)
	ifsc = models.CharField(blank=True,null=True,verbose_name='IFSC Code',max_length=11)
	contact_id = models.CharField(blank=True,null=True,verbose_name='Contact ID',max_length=100)
	fund_id = models.CharField(blank=True,null=True,verbose_name='Fund Account ID',max_length=100)
	date = models.DateTimeField(auto_now=True,verbose_name='Date Edited')
	def __str__(self):
		return 'Fund Account of '+self.user.name
	
	def save(self, *args, **kwargs):
		session = requests.Session()
		session.auth = (TEST_RAZOR_KEY_ID, TEST_RAZOR_KEY_SECRET)
		data = {
			"name": self.user.name,
			"email": self.user.email,
			"contact": self.user.contact if self.user.contact else None,
			"type": "customer",
		}
		response = session.post('https://api.razorpay.com/v1/contacts', data=json.dumps(data), headers={'Content-Type': 'application/json'})
		content = json.loads(response.content.decode('utf-8'))
		print(content, type(content))
		if 'id' in content:
			self.contact_id = content['id']
			data2 = {
				"contact_id": content['id'],
				"account_type": self.type
			}
			if self.type == 'vpa':
				data2['vpa'] = {
					"address": self.upi
				}
			elif self.type == 'bank_account':
				data2["bank_account"] = {
					"name": self.name,
					"ifsc": self.ifsc,
					"account_number": self.accountno
				}
			else:
				print('again error at funding',self.type)
			response2 = session.post('https://api.razorpay.com/v1/fund_accounts', data=json.dumps(data2), headers={'Content-Type': 'application/json'})
			content2 = json.loads(response2.content.decode('utf-8'))
			print(content2, type(content2))
			if 'id' in content2:
				self.fund_id = content2['id']
			else:
				print('error at fund account req',self.type, data2)
		else:
			print('error at contact')
		super(FundAccount, self).save(*args, **kwargs)


	class Meta:
		verbose_name_plural = 'Fund Accounts'
