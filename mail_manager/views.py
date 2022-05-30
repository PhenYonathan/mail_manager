from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "mail_manager/index.html"

    def post(self, request, **kwargs):
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            # return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
            return redirect('app_home')

        return render(request, self.template_name)


class LogoutView(TemplateView):
    template_name = "mail_manager/index.html"

    def get(self, request, **kwargs):
        logout(request)

        return render(request, self.template_name)
