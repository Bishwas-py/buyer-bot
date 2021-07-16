from django.shortcuts import render
from.models import Items

def home(request):
    return render(request, "bots/index.html")

# def settings(request):
#     items = Items.objects.all()
#     context = {
#         "items":items,
#     }
#     return render(request, "bots/index.html",context)
