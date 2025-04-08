import threading
from threading import Thread
from django.core.mail import EmailMessage
from honeb.settings import EMAIL_HOST_NAME
from django.template.loader import get_template


class EmailThread(threading.Thread):
    def __init__(self, subject, template, context, res,attach,attach2=[]):
        self.subject = subject
        self.res = res
        self.template = template
        self.context = context
        self.attach = attach
        self.attach2 = attach2
        threading.Thread.__init__(self)

    def run (self):
        template = get_template(self.template)
        content = template.render(self.context)
        msg = EmailMessage(self.subject, content, EMAIL_HOST_NAME, [],self.res)
        # print(self.attach)
        for a in self.attach:
            msg.attach(a['name'],a['file'],a['type'])
        if self.attach2:
            msg.attach(self.attach2['name'],self.attach2['file'],self.attach2['type'])
        msg.content_subtype = "html"
        # print('sending')
        msg.send()

def send_html_mail(subject, context, template, recipient_list,recipient_list2,attach,attach2):
    # print('entered')
    recipient_list += recipient_list2
    EmailThread(subject, template, context, recipient_list,attach,attach2).start()