from django.contrib import admin
from django.http import HttpResponse, HttpResponseRedirect
from .models import Bounty, FundAccount, Notification
from django.contrib import messages
from django.utils.html import format_html

from django.utils.timesince import timesince
from django.urls import path
import requests
import json
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
# Register your models here.
import razorpay
from django.utils import timezone


razorpay_client = razorpay.Client(
    auth=(settings.TEST_RAZOR_KEY_ID, settings.TEST_RAZOR_KEY_SECRET))
class BountyAdmin(admin.ModelAdmin):
    list_display = ['bt','bf','amountt','reportt','status','payout']
    search_fields = ['fro__name','fro__username','to__name','to__username','amount','report__title']
    list_filter = ['date', 'requested', 'claimed', 'reqdate', 'cldate']
    def bf(self, obj):
        return obj.fro.name
    def amountt(self, obj):
        return '₹'+str(obj.amount)
    def reportt(self, obj):
        return obj.report.title
    def bt(self, obj):
        return obj.to.name
    def status(self, obj):
        if obj.paid:
            if obj.claimed:
                return 'Claimed '+str(timesince(obj.cldate) if obj.cldate else '')+' ago'
            elif not obj.claimed and obj.requested:
                return 'Requested '+str(timesince(obj.reqdate) if obj.reqdate else '')+' ago'
            else:
                return 'Received but not claimed'
        else:
            return 'Invalid'
    #URLS
    def get_urls(self):
            urls2 = [
                path('paybounty', self.paybounty, name='pay-bounty'),
            ]
            urls = super().get_urls()
            urls2 += urls
            return urls2

    def paybounty(self, request, **kwargs):
        if request.user.is_authenticated:
            try:
                id = request.GET['id']
            except:
                messages.error(request, 'Please select bounty first')
                return HttpResponseRedirect('/panel/')
            try:
                bounty = Bounty.objects.get(id=id)
            except Exception as e:
                print(e)
                messages.error(request, 'Please select bounty first')
                return HttpResponseRedirect('/panel/')
            try:
                bounty.to.account
            except ObjectDoesNotExist:
                messages.error(request, 'The User does not have Fund Account attached')
                return HttpResponseRedirect('/panel/')
            if request.user.is_admin:
                session = requests.Session()
                session.auth = (settings.TEST_RAZOR_KEY_ID, settings.TEST_RAZOR_KEY_SECRET)
                data = {
                    "account_number": "2323230078386402",
                    "fund_account_id": bounty.to.account.fund_id,
                    "amount": int(bounty.amount*100),
                    "currency": "INR",
                    "mode": "UPI" if bounty.to.account.type == 'vpa' else 'NEFT',
                    "purpose": "payout",
                    "queue_if_low_balance": True,
                    "narration": "Admin Payout to User",
                }
                response = session.post('https://api.razorpay.com/v1/payouts', 
                data=json.dumps(data), 
                headers={'Content-Type': 'application/json'})
                print(response.content)
                content = json.loads(response.content)
                if content["error"]["code"] == "NA":
                    bounty.claimed = True
                    bounty.cldate = timezone.now()
                    bounty.save()
                    messages.success(request, 'Payout successfully sent')
                    return HttpResponseRedirect('/panel/other/bounty')
                else:
                    messages.error(request, 'Payout unsuccessful')
                    return HttpResponseRedirect('/panel/other/bounty')
                return HttpResponse(json.dumps(json.loads(content), indent=4, sort_keys=True))
        else:
            return HttpResponseRedirect('/panel/')
    def payout(self, obj):
        return format_html(f'''<a href="paybounty?id={obj.id}" class="btn btn-sm btn-success">Pay</a>''') if obj.requested and not obj.claimed else ''
    bf.short_description = 'Sent By'
    bt.short_description = 'Receiver'
    amountt.short_description = 'Amount'
    reportt.short_description = 'Report'
    bf.admin_order_field = 'fro__name'
    bt.admin_order_field = 'to__name'
    amountt.admin_order_field = 'amount'
    reportt.admin_order_field = 'report__title'
admin.site.register(Bounty, BountyAdmin)

class FundAccountAdmin(admin.ModelAdmin):
    list_display = ['userv','typee','date']
    search_fields = ['user__name','user__username']
    list_filter = ['type','date']
    def typee(self, obj):
        return obj.get_type_display()
    def userv(self, obj):
        return 'Fund account of '+ obj.user.name
    typee.short_description = 'Account Type'
    typee.admin_order_field = 'type'
    userv.short_description = 'Account'
    userv.admin_order_field = 'user__name'
admin.site.register(FundAccount, FundAccountAdmin)


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['userv','title','pdate']
    search_fields = ['of__name','of__username']
    list_filter = ['ntype','pdate']
    autocomplete_fields = ['of']
    exclude = ['type','user','seen']
    def typee(self, obj):
        return obj.get_type_display()
    def userv(self, obj):
        return 'Notification for '+ (obj.of.name if obj.of.name else obj.of.username)
    typee.short_description = 'Account Type'
    typee.admin_order_field = 'ntype'
    userv.short_description = 'Notification'
    userv.admin_order_field = 'of__name'
admin.site.register(Notification, NotificationAdmin)

            # response = session.post('https://api.razorpay.com/v1/fund_accounts', 

            # claim = razorpay_client.payment.transfer(dict(amount=int(100),currency='INR', payment_capture='0'))






            # print(claim)
            # print(request.data)








                # "fund_account_id": "fa_JhgaoJqionKt0c",
            # data = {
            #     # "name": "Vivek Billa",
            #     # "email": "vivekbilla345@gmail.com",
            #     # "contact": "9136247408",
            #     "account_type": "vpa",
            #     "contact_id": "cont_JhgZk5XnFvltq4",
            #     "vpa":{
            #         "address":"9136247408@paytm"
            #     }
            # }