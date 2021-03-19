from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def user_directory(request):
    template = loader.get_template('sysadmin/user-directory.html')
    # Any additional data needed
    context = {}
    return HttpResponse(template.render(context, request))