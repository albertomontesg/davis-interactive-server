import binascii
import os

from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.forms import ModelForm
from django.utils import timezone


class Participant(models.Model):
    user_id = models.CharField(
        max_length=128, unique=True, primary_key=True, blank=False, null=False)
    name = models.CharField(max_length=254, blank=False, null=False)
    organization = models.CharField(max_length=254, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    registration_datetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.name} ({self.organization})'

    def generate_key(self):
        self.user_id = binascii.hexlify(os.urandom(32)).decode()
        return self

    def email_participant(self, subject, message):
        send_mail(
            subject,
            message,
            settings.EMAIL_FROM, [self.email],
            fail_silently=False)


class RegistrationForm(ModelForm):
    name = forms.CharField(min_length=4, label='Full Name')
    organization = forms.CharField(
        min_length=2, label='Organization/Affiliation')
    email = forms.EmailField(label='E-mail')

    class Meta:
        model = Participant
        fields = ['name', 'organization', 'email']
