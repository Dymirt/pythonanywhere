from django.forms import model_to_dict
from django.shortcuts import render
from .forms import MessageFrom
from django.http import JsonResponse
from django.core.mail import send_mail
import os
# Create your views here.


def index(request):
    return render(request, "resume/index.html", {'form': MessageFrom()})


def send_message(request):
    if request.method == "POST":

        form = MessageFrom(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            send_mail(
                f'New message on personal website',
                f'{instance.email} \n {instance.message} \n {instance.name}',
                '',
                [os.getenv("EMAIL_HOST_USER")],
                fail_silently=False,
            )
            instance.save()
            # converts Post instance to dictionary so JsonResponse can serialize it to Json
            return JsonResponse(
                model_to_dict(instance, fields=['name']), status=201)
        else:
            return JsonResponse(form.errors, safe=False, status=200)