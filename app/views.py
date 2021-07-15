from django.shortcuts import render

def home(request):
    return render(request, "index.html")

def settings(request):
    return render(request, "settings.html")

def add_links(request):
    return render(request, "add_links.html")