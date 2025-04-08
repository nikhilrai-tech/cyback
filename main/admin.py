from django.contrib import admin
from .models import *
from django.http import HttpResponseRedirect, request
from django.utils.html import format_html
from django import forms
from django.contrib.admin.widgets import AutocompleteSelect
from django.db.models.query_utils import Q
from .weakness import weaknesses
from django.utils.timesince import timesince
import re
# Register your models here.


def markdown(markd):
    def getstring(str):
        str2 = '<span>'
        for st in str:
            if st == '[':
                str2 += '<a href="'
            elif st==',':
                str2 += '">'
            elif st==']':
                str2 += '</a>'
            else:
                str2+= st
        str2+='<span>'
        return str2
    marks = markd.split('\n')
  #  print(marks)
    string = ''
    for i in marks:
        if len(i) > 0:
            if i[0] == '#':
                string+=f'<h1 class="mb-1 font-weight-bolder">{getstring(i[1:])}</h1>'
            else:
                string+=f'<div>{getstring(i)}</div>'
    return string


class ReportInline(admin.StackedInline):
    model = Report
    readonly_fields = ('main',)
    def main(self,obj):
        stre = '<div class="d-flex flex-column">'
        stre += f'''<div class="d-flex user-linkc mb-3">
        <a href="/panel/back/user/{obj.posted_by.id}/change/">
        <div class="user-link ">
        <span class="{'active' if obj.posted_by.is_active else 'inactive'}" rel="tooltip" title="" data-original-title="{'Active' if obj.posted_by.is_active else 'Freezed'}"></span>
        <img src="{obj.posted_by.photo.url if obj.posted_by.photo else '/static/user.jpg'}" width="25" height="25" style="width: 25px !important;">
        <p>{obj.posted_by.username}</p>
        </div>
        </a>
        </div>
        '''
        stre += f'''<div class="d-flex mb-2"><a href="/panel/main/report/{obj.id}/change"><h2 class="mb-0 mr-2" style="font-weight: 600; font-size: 1.4875rem;">{obj.title}</h2></a>
        <div class="rounded-pill bg-primary px-2 py-1 mr-1"><a href="/panel/main/scope/{obj.asset.id}/change/" class="mb-0 text-white">{obj.asset.get_type_display()} | {obj.asset.domain}</a></div>'''
        if obj.disclosure:
            stre += '<img src="/static/admin/img/icon-yes.svg" alt="Publicly Disclosed">'
        stre+='</div>'
        weaklist = [e["name"] for e in weaknesses if str(e['id']) == obj.weakness]
        if len(weaklist) == 0:
            stre += f'<p>  [{obj.get_status_display()}]</p>'
        elif len(weaklist) > 1:
            stre += f'<p> [{obj.get_status_display()}]</p>'
        else:
            stre += f'<p>{weaklist[0]}  <span class="text-error">[{obj.get_status_display()}]</span></p>'
        stre += '<div class="d-flex" >'
        stre += f'''<button class="btn btn-info btn-sm btn-simple" data-toggle="modal" data-target="#desc{obj.id}">Description</button>
        <div class="card-type  type-{obj.get_severity_display()}" rel="tooltip" title="" data-original-title="Severity: {obj.get_severity_display()}"></div>
        <div class="modal fade" id="desc{obj.id}" tabindex="-1" role="dialog">
            <div class="modal-dialog" role="document">
              <div class="modal-content">
                <div class="modal-header pb-2">
                    <h2 class="mb-0">Description</h2>
                </div>
                <hr class="w-100 mb-0">
                <div class="modal-header pb-4 flex-column">
                    {markdown(obj.description)}
                </div>
              </div>
            </div>
        </div>
        <button class="btn btn-info btn-sm btn-simple" data-toggle="modal" data-target="#report{obj.id}">Impact</button>
        <div class="modal fade" id="report{obj.id}" tabindex="-1" role="dialog">
            <div class="modal-dialog" role="document">
              <div class="modal-content">
                <div class="modal-header pb-2">
                    <h2 class="mb-0">Impact</h2>
                </div>
                <hr class="w-100 mb-0">
                <div class="modal-header pb-4 flex-column">
                    {markdown(obj.impact)}
                </div>
              </div>
            </div>
        </div>
        '''
        stre+='</div>'
        stre+='<hr class="w-100">'
        imagestr = '<div class=" d-flex">'
        if obj.photo0:
            imagestr+=f'<img src="{obj.photo0.url}" alt="Attached image 1" height="50" width="50" style="object-fit: cover; width: 50px; margin-right: 5px;" />'
        if obj.photo1:
            imagestr+=f'<img src="{obj.photo1.url}" alt="Attached image 2" height="50" width="50" style="object-fit: cover; width: 50px; margin-right: 5px;" />'
        if obj.photo2:
            imagestr+=f'<img src="{obj.photo2.url}" alt="Attached image 3" height="50" width="50" style="object-fit: cover; width: 50px; margin-right: 5px;" />'
        imagestr += '</div>'
        stre += imagestr
        stre+='</div>'
        return format_html(stre)
    exclude = ['posted_by','photo0','photo1','photo2','impact','description','severity','title','weakness','disclosure','asset','status']
    def get_extra(self, request, obj=None, **kwargs):
        return 0







class CommentInline(admin.StackedInline):
    model = Comment
    readonly_fields = ('main',)
    def main(self,obj):
        stre = '<div class="d-flex flex-column">'
        stre += f'''<div>
        <div class="d-flex user-linkc mb-3 {obj.type}">
        <a href="/panel/back/user/{obj.posted_by.id}/change/">
        <div class="user-link ">
        <span class="{'active' if obj.posted_by.is_active else 'inactive'}" rel="tooltip" title="" data-original-title="{'Active' if obj.posted_by.is_active else 'Freezed'}"></span>
        <img src="{obj.posted_by.photo.url if obj.posted_by.photo else '/static/user.jpg'}" width="25" height="25" style="width: 25px !important;">
        <p>{obj.posted_by.username}</p>
        </div>
        </a>
        </div>
        '''
        stre+='<p>'
        if obj.request:
            if obj.type == 'D':
                stre+='requested for Public Disclosure'
            elif obj.type == 'A':
                stre+='requested for Status Change'
            elif obj.type == 'B':
                stre+='added a comment'
            else:
                stre+='commented'
        else:
            if obj.type == 'D':
                stre+='made this report Public'
            elif obj.type == 'D2':
                stre+='made this report Hidden'
            elif obj.type == 'A':
                stre+='changed status to '
            elif obj.type == 'B':
                stre+='added a comment'
            else:
                stre+='commented'
        stre+=f' {timesince(obj.date)} ago</p></div>'
        # stre+='</div>'
        if obj.type == 'B':
            stre+=f'<hr class="w-100"><div>{markdown(obj.body)}</div>'
        stre+='</div>'
        return format_html(stre)
    exclude = ['posted_by','body','request','type']
    def get_extra(self, request, obj=None, **kwargs):
        return -1
    def get_queryset(self, request):
        qs = super(CommentInline, self).get_queryset(request)
        return qs.order_by('-date')











class ProgramAdmin(admin.ModelAdmin):
    inlines = [ReportInline]
    list_display = ['programv','userv','bounty','scoping','managed', 'type', 'splitting']
    list_filter = ['type','active','managed','updated','splitting','published','lastedited']
    search_fields = ['scopes','thanks','subscribed']
    exclude = ['resolved','efficiency','thanks','subscribed','posted_by','scopes','updated','lowreward','midreward', 'highreward','criticreward',
    'active','title','type','policy','managed','splitting','background']
    readonly_fields = ['program','policyc','scoping','rewards','posted','invited']

    def invited(self, obj):
        # print(obj.type)
        if obj.type =='PRI':
            stringf = ''
            for user in obj.subscribed.all():
                # print(user)
                stringf += '<a href="/panel/back/user/%s/change">%s</a>, '%(user.id,'' if not re.match("^[a-zA-Z0-9_@ .-]+$", user.name) else user.name)
                # print(stringf)
            return format_html(stringf)
        else:
            return '-'
    def policyc(self,obj):
        return format_html(markdown(obj.policy))
    def rewards(self,obj):
        return format_html(f'''<div><span class="mr-3" rel="tooltip" data-original-title="Lowest">₹ {obj.lowreward}</span> | 
        <span class="mx-3" rel="tooltip" data-original-title="Mid">₹ {obj.midreward}</span> | 
        <span class="mx-3" rel="tooltip" data-original-title="High">₹ {obj.highreward}</span> | 
        <span class="ml-3" rel="tooltip" data-original-title="Critical">₹ {obj.criticreward}</span></div>''')
    
    def posted(self,obj):
        return format_html(f'''<div class="d-flex user-linkc mb-3">
        <a href="/panel/back/user/{obj.posted_by.id}/change/">
        <div class="user-link ">
        <span class="{'active' if obj.posted_by.is_active else 'inactive'}" rel="tooltip" title="" data-original-title="{'Active' if obj.posted_by.is_active else 'Freezed'}"></span>
        <img src="{obj.posted_by.photo.url if obj.posted_by.photo else '/static/user.jpg'}" width="25" height="25" style="width: 25px !important;">
        <p>{obj.posted_by.username}</p>
        </div>
        </a>
        </div>''')
    
    def program(self,obj):
        stre = '<div class="d-flex flex-column">'
        stre += f'''<div class="d-flex mb-2"><h2 class="mb-0 mr-2" style="font-weight: 600; font-size: 1.4875rem;">{obj.title}</h2>
        <div class="rounded-pill border border-warning px-2 py-1 mr-1"><p class="mb-0 text-warning">{obj.get_type_display()}</p></div>'''
        if obj.splitting:
            stre += '<img src="/static/admin/img/icon-yes.svg" rel="tooltip" data-original-title="Bounty Splitting Eligible" alt="Bounty Splitting Eligible">'
        if obj.managed:
            stre += '<img src="/static/logo.png" alt="Managed By Cyber3ra">'
        stre+='</div>'
        if obj.background:
            stre+=f'<div class="w-100"><img src="{obj.background.url}" class="w-100" style="height: 150px; object-fit: cover;" /></div>'
        stre+='</div>'
        return format_html(stre)
    
    def get_actions(self, request):
        actions = super(ProgramAdmin, self).get_actions(request)
      #  print(self.model.posted_by)
        return actions
    
    #HTML FORMATTING
    def scoping(self, obj):
        scs = {}
        string = '<div class="d-flex">'
        for sc in obj.scopes.all():
            if sc.get_type_display() in scs.keys():
                scs[sc.get_type_display()] += 1
            else:
                scs[sc.get_type_display()] = 1
        # print(scs)
        for key in scs.keys():
            string+='<div class="rounded-pill bg-primary px-2 py-1 mr-1"><p class="mb-0">%s | %s</p></div>'%(key,scs[key])
        string += '</div>'
        # print(string)
        return format_html(string)

    def bounty(self, obj):
        if obj.lowreward and obj.criticreward:
            return format_html('<span rel="tooltip" title="Lowest Bounty">₹ %s</span> - <span rel="tooltip" title="Highest Bounty">₹ %s</span>'%(obj.lowreward,obj.criticreward))
        else:
            'No Bounty available'

    def userv(self, obj):
        return format_html('<div class="user-link "><img src="%s" width="25" height="25" ><p class="text-white">%s</p></div>'%(
            obj.posted_by.photo.url if obj.posted_by.photo else '/static/user.jpg',obj.posted_by.username))
        
    def titlep(self, obj):
        return format_html('<div class="text-white">%s%s</div>'%(obj.get_type_display(),'<img src="/static/admin/img/icon-yes.svg" alt="Managed by Cyber3ra" title="Managed By Cyber3ra" rel="tooltip" class="ml-1">' if obj.managed else ''))



    def programv(self, obj):
        return format_html('<div class="user-link "><img src="%s" width="40" height="40" style="border-radius: 4px;" ><p class="text-white">%s</p></div>'%(
            # obj.id, <a href="/panel/main/program/%s/change"> </a>
            obj.background.url if obj.background else '/static/user.jpg',obj.title))

    programv.short_description = 'Program'
    programv.admin_order_field = 'program__title'
    userv.short_description = 'Posted By'
    userv.admin_order_field = 'posted_by__username'
    titlep.short_description = 'Program'
    titlep.admin_order_field = 'type'
    bounty.admin_order_field = 'lowreward'
    scoping.short_description = 'Scopes'
    policyc.short_description = 'Policy'
    posted.short_description = 'Posted By'
        
    # def delete_queryset(self, request, queryset):
        # for obj in queryset:
        #     obj.delete()
        # pass


class ScopeAdmin(admin.ModelAdmin):
    exclude = ['company']
    # form = ScopeForm
    list_display = ['type','domain','severity']
    search_fields = ['type','domain']
    def get_search_results(self, request, queryset, search_term):
        if len(search_term) > 0:
            results = ( [ x for x, y in enumerate(Scope.MAIN_CHOICES, start=1) if search_term.lower() in y[1].lower()] )
            if request.user.type == 'Ct':
                if request.user.refuser:
                        queryset = Scope.objects.filter(Q(company=request.user.refuser)&(Q(type__in=results)|Q(domain__contains=search_term))).order_by('-id')
                else:
                    queryset = Scope.objects.filter(Q(company=request.user)&(Q(type__in=results)|Q(domain__contains=search_term))).order_by('-id')
            else:
                queryset = Scope.objects.filter(Q(company=request.user)&(Q(type__in=results)|Q(domain__contains=search_term))).order_by('-id')
            # print(queryset)
            return queryset, search_term
        else:
            return Scope.objects.filter(company=request.user).order_by('-id'), False
    def save_model(self, request, obj, form, change):
        if not change:
            if request.user.type == 'Ct':
                obj.company = request.user.refuser
            else:
                obj.company = request.user
        super().save_model(request, obj, form, change)






class JobAdmin(admin.ModelAdmin):
    list_display = ['designation','linka','atype','posted_by','location','remote','out','published','lasteditedc']
    exclude = ['posted_by']

    def desc(self,obj):
        return format_html(obj.description)
    desc.short_description = 'Description'

    def lasteditedc(self, obj):
        return timesince(obj.lastedited)+ ' ago'
    lasteditedc.short_description = 'Last Edited'
    def linka(self, obj):
        if obj.link:
            return format_html('<a href="%s" target="_blank" class="btn btn-sm btn-error">Go</a>'%(obj.link))
        else:
            return '-'
    

    def atype(self, obj):
        return obj.get_type_display()
    


class ReportAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
    list_display = ['reportv','userv','programv','scoping','disclosure']
    list_filter = ['status','disclosure','severity']
    search_fields = ['title','posted_by__username','program__title']

    
    #HTML FORMATTING
    def scoping(self, obj):
        scs = {}
        string = '<div class="d-flex"><div class="rounded-pill bg-primary px-2 py-1 mr-1"><p class="mb-0">%s | %s</p></div></div>'%(obj.asset.get_type_display(),obj.asset.domain)
        # print(string)
        return format_html(string)

    def userv(self, obj):
        return format_html('<a href="/panel/back/user/%s/change"><div class="user-link "><img src="%s" width="25" height="25" ><p class="text-white">%s</p></div></a>'%(obj.posted_by.id,
            obj.posted_by.photo.url if obj.posted_by.photo else '/static/user.jpg',obj.posted_by.username))

    def programv(self, obj):
        return format_html('<a href="/panel/main/program/%s/change"><div class="user-link "><img src="%s" width="40" height="40" style="border-radius: 4px;" ><p class="text-white">%s</p></div></a>'%(obj.program.id,
            obj.program.background.url if obj.program.background else '/static/user.jpg',obj.program.title))

    def reportv(self, obj):
        return format_html(f'#{obj.id} : {obj.title}')
    scoping.short_description = 'Scope'

    # def has_view_permission(self, request, obj=None):
    #     if obj:
    #         print('here')
    #         if request.user.type == 'U':
    #             print(obj.posted_by.id == request.user.id)
    #     else:
    #         return request.user.is_superadmin
    #     return False

    programv.short_description = 'Program'
    programv.admin_order_field = 'program__title'
    reportv.short_description = 'Report'
    reportv.admin_order_field = 'title'
    userv.short_description = 'Posted By'
    userv.admin_order_field = 'posted_by__username'


admin.site.register(Program,ProgramAdmin)
# admin.site.register(Scope, ScopeAdmin)
# admin.site.register(Thanks)
admin.site.register(Job, JobAdmin)
admin.site.register(Report, ReportAdmin)

