from django import template
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from django.views import generic


class IndexView(generic.ListView):
    template_name = 'sysadmin/user_list.html'
    context_object_name = 'user_list'

    def get_queryset(self):
        return User.objects.all()

def user_directory(request):
    template = loader.get_template('sysadmin/users.html')
    # Any additional data needed
    context = {}
    return HttpResponse(template.render(context, request))