from sysadmin.forms import CustomUserCreationForm
from django import template
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.urls import reverse

from django.db.models import Q


def user_list(request):
    search_term = request.GET.get('search_term')
    if(search_term is None or search_term == ''):
        user_list = User.objects.all()
        search_term = ''
    else:
        user_list = User.objects.filter(Q(email__icontains = search_term) |Q(first_name__icontains = search_term) | Q(last_name__icontains = search_term))
    # template = loader.get_template('polls/index.html')
    context = { 'user_list' : user_list, 'search_term' :search_term}
    # return HttpResponse(template.render(context,request))
    return render(request, 'sysadmin/user_list.html',context)


def create_user(request):
    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')
            return HttpResponseRedirect(reverse('sysadmin:create-user'))
    else:
        f = CustomUserCreationForm()

    return render(request, 'sysadmin/create_user.html', {'form': f})
