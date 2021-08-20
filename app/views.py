from django.shortcuts import redirect, render
from django.urls import reverse
from.models import Items
from.machine.main import quit_all_bot, threader, threads, quit_bot, run_isolated_bot

def home(request):
    return render(request, "bots/index.html", {"threads":threads})

def start_bots(request):
    if not threads:
        threader()
    return redirect(reverse('dashboard'))

def stop_bots(request, id:int):
    quit_bot(id)
    return redirect(reverse('dashboard'))

def stop_all_bots(request):
    quit_all_bot()
    return redirect(reverse('dashboard'))


def start_iso_bot(request, id:int):
    run_isolated_bot(id)
    return redirect(reverse('dashboard'))

def clear_bots(request):
    quit_all_bot()
    threads.clear()
    return redirect(reverse('dashboard'))
    