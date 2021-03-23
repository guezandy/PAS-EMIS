from django import template
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse

from django.db.models import Q
from sysadmin.forms.user_create import CustomUserCreationForm
from sysadmin.forms.user_detail import CustomEditUserForm

def user_list(request):
    search_term = request.GET.get('search_term')
    if(search_term is None or search_term == ''):
        user_list = User.objects.all()
        search_term = ''
    else:
        user_list = User.objects.filter(Q(username__icontains = search_term) |Q(email__icontains = search_term) |Q(first_name__icontains = search_term) | Q(last_name__icontains = search_term))
    context = { 'user_list' : user_list, 'search_term' :search_term}
    return render(request, 'sysadmin/user_list.html',context)


def create_user(request):
    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'User created successfully')
            return HttpResponseRedirect(reverse('sysadmin:create-user'))
    else:
        f = CustomUserCreationForm()

    return render(request, 'sysadmin/user_create.html', {'form': f})

def user_detail(request, pk: int):
    if request.method == 'POST':
        user = get_object_or_404(User, pk= pk)
        f = CustomEditUserForm(request.POST, instance=user)
        if f.is_valid():
            f.save()
            messages.success(request, 'User updated successfully')
            return HttpResponseRedirect(reverse('sysadmin:user-detail', args=(pk,)))
    else:
        user = get_object_or_404(User, pk= pk)
        f = CustomEditUserForm(instance=user)

    return render(request, 'sysadmin/user_detail.html', {'form': f})

