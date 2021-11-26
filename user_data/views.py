"""
Django views for user_data app.

Generated by 'manage.py startapp' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/http/views/
"""

from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import RegisterForm


def register(request):
    """register view"""

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse("qcm:index"))

    else:
        form = RegisterForm()

    return render(request, "user_data/register.html", {"form": form})
