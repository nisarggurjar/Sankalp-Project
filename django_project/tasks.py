from __future__ import absolute_import, unicode_literals
import random


from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage
from django.conf import settings
from django.template.loader import get_template, render_to_string

def Send_Mail_Task(name, email, mobile, year, branch, course, messege):
    from_email = settings.EMAIL_HOST_USER
    to_email = ['prateek29mishra@gmail.com']
    d = {
        'name':name, 'email':email,
        'mobile':mobile, 'year':year,
        'course':course,
        'branch':branch, 'messege':messege
    }
    html = get_template("registration_mail.html").render(d)
    msg = EmailMultiAlternatives("TechSim+ - New Enquiry", " ", from_email, to_email)
    msg.attach_alternative(html, "text/html")
    msg.send()


def add(name, email, course, number):
    from_email = settings.EMAIL_HOST_USER
    to_email = [email]
    d = {
        'name':name,
        'number':number,'course':course,
    }
    html = get_template("mail.html").render(d)
    msg = EmailMultiAlternatives("TechSim+ - Certificate", " ", from_email, to_email)
    msg.attach_alternative(html, "text/html")
    msg.send()