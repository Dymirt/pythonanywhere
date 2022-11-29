from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import MessageFrom

# Create your views here.


def index(request):

    if request.method == "GET":
        form = MessageFrom(initial={'user': request.user})
    else:
        form = MessageFrom(request.POST)
        if form.is_valid():
            form.save()
            form.clean()
    return render(request, "resume/index.html", {'form': form})
