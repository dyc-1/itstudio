from django.shortcuts import render, redirect, reverse


def home(request):
    return render(request, 'index.html', locals())


def redirectHome(request):
    return redirect(reverse('myindex'))
