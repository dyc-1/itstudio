from django.shortcuts import render, redirect, reverse
from untils.configs import get_ip


def home(request):
    request.session['ip'] = get_ip(request)
    request.session['ban'] = "1"
    return render(request, 'index.html', locals())


def redirectHome(request):
    request.session['ip'] = get_ip(request)
    request.session['ban'] = "1"
    return redirect(reverse('myindex'))
