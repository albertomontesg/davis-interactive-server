from django.shortcuts import redirect, render
from django.views.generic.edit import FormView

from .models import RegistrationForm


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            participant = form.save(commit=False)
            participant.generate_key()
            participant.save()

            return render(request, 'success.html')
    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})


def success(request):
    return render(request, 'success.html')
