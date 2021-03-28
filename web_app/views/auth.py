from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.signing import TimestampSigner
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404

from web_app.forms.auth import ActivationForm, SignUpForm
from sysadmin.models import Activation

def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('web_app:index')
    else:
        form = SignUpForm()
    return render(request, 'web_app/auth/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect('web_app:index')
    form = AuthenticationForm()
    return render(request, 'web_app/auth/login.html', {'form': form})

def activation_view(request, code: str):
    if request.method == 'POST':
        form = ActivationForm(user = None,data = request.POST)
        activation_record = get_object_or_404(Activation, code=code)
        form.user = activation_record.user
        code_is_valid(code,request.POST['email'],activation_record.user)
        if form.is_valid():
            try:
                signer = TimestampSigner()
                plain_text_email = signer.unsign(request.POST.get('email') + ':' + activation_record.code)
                if(plain_text_email == request.POST.get('email') and plain_text_email == form.user.email):
                    form.user.is_active = True
                    form.save() # save the activation form (password set)
                    form.user.save() # save the users is_active flag
                    
                    user = authenticate(request, username=form.user.username, password=form.data['new_password1'])
                    if user is not None and user.is_active:
                        activation_record.delete() # delete the activation record so it can no longer be used
                        login(request, user)
                        redirect('web_app:index')
                else:
                    form.add_error(None, 'The code or email provided was invalid.')      
            except:
               form.add_error(None, 'The code or email provided was invalid.')
    else:
        form = ActivationForm(None)
    return render(request, 'web_app/auth/activation.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('web_app:index')

def code_is_valid(code:str, email:str, user: User):
    max_days = 7 # expires in 7 days
    max_seconds = max_days * 24 * 60 * 60

    signer = TimestampSigner()
    try:
        signed_text = signer.unsign(email + ":" + code, max_age= max_seconds)
        return signed_text == email
    except:
        return False