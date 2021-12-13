"""
Django views for user
"""
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from ..forms import RegisterForm


def register_view(request):
    """register view"""

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("user_data:index"))

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse("login"))

    else:
        form = RegisterForm()

    return render(request, "user_data/register.html", {"form": form})
