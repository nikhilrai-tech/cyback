from other.models import Notification
from back.email import send_html_mail

def add_noti_single(user,title,body,type='O',ntype='I',link='#',avatar=None):
  #  print(avatar)
    noti = Notification(title=title,body=body,type=type,ntype=ntype,link=link,of=user, user=avatar)
    noti.save()

def add_noti_single_email(user,title,body,type='O',ntype='I',link='#',avatar=None):
  #  print(avatar)
    noti = Notification(title=title,body=body,type=type,ntype=ntype,link=link,of=user, user=avatar)
    noti.save()
    send_html_mail(title,{"name": user.name if user.name else user.username,"message": body},"email/desc.html",[user.email],[],[],[])

def add_noti_multiple(users,title,body,type='O',ntype='I',link='#',avatar=None):
    for user in users:
        noti = Notification(title=title,body=body,type=type,ntype=ntype,link=link,of=user, user=avatar)
        noti.save()

def add_noti_multiple_email(users,title,body,type='O',ntype='I',link='#',avatar=None):
    for user in users:
        noti = Notification(title=title,body=body,type=type,ntype=ntype,link=link,of=user, user=avatar)
        noti.save()
        send_html_mail(title,{"name": user.name if user.name else user.username,"message": body},"email/desc.html",[user.email],[],[],[])