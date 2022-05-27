from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.http import Http404

# Create your views here.
from django.views.generic import TemplateView, ListView

from app_manager.models import GetMails


# @method_decorator(login_required, name='dispatch')
class HomeAppView(TemplateView):
    template_name = "app_manager/index.html"


# @method_decorator(login_required, name='dispatch')
class AppMoreInfos(ListView):
    model = GetMails
    template_name = "app_manager/more_infos.html"

