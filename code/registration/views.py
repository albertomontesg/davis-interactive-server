from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.views.generic.edit import FormView

from .models import RegistrationForm


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            participant = form.save(commit=False)
            participant.generate_key()
            message = render_to_string('registration_email.html',
                                       {'participant': participant})

            participant.email_participant('DAVIS Challenge Registration',
                                          message)
            participant.save()

            return render(request, 'success.html', {'participant': participant})
    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})
