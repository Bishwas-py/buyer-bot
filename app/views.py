from django.shortcuts import render
from.models import Items
from.machine.main import threader, threads

def home(request):
    return render(request, "bots/index.html")

def start_bots(request):
    if not threads:
        print("Thread started")
        threader()
    return render(request, "bots/running.html", {"threads":threads})
        