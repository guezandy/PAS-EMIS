from django.core.mail.message import EmailMultiAlternatives
from authentication.models.forgot_password import ForgotPassword
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.core.signing import TimestampSigner
from django.db.models.query_utils import Q
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.urls.base import reverse
from django.core.exceptions import PermissionDenied
from django.template.loader import get_template
from django.conf import settings
from authentication.models.users import get_user_type

from authentication.forms.auth import (
    CustomSetPasswordForm,
    SignUpForm,
    UserEditSelfForm,
    ForgotPasswordForm,
)
from authentication.models.activation import Activation
from authentication.views import auth

from authentication.models.users import Teacher
from datetime import date, timedelta


import logging

LOGGER = logging.getLogger("emis-pas")


def index(request):
    user_type_entry_message = {
        "custom": {"header": "Super user", "content": "Add content here"},
        "teacher": {"header": "", "content": ""},
        "school_admin": {"header": "", "content": ""},
        "principal": {"header": "", "content": ""},
        "district_officer": {"header": "", "content": ""},
        "school_superviser": {"header": "", "content": ""},
        "stat_admin": {"header": "", "content": ""},
        "evaluation_admin": {"header": "", "content": ""},
        "early_childhood_educator": {"header": "", "content": ""},
        "support_services_admin": {"header": "", "content": ""},
        "external_accessor": {"header": "", "content": ""},
    }
    if request.user and request.user.is_authenticated:
        user_type, parent_user = get_user_type(request.user)
        return render(request, "index.html", user_type_entry_message.get(user_type))
    return render(request, "authentication/index.html", {})


def register_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            raw_password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(auth.index)
    else:
        form = SignUpForm()
    return render(request, "authentication/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return redirect(auth.index)
    else:
        form = AuthenticationForm()
    return render(request, "authentication/login.html", {"form": form})


def activation_view(request, code: str):
    if request.method == "POST":
        form = CustomSetPasswordForm(user=None, data=request.POST)
        activation_record_results = Activation.objects.filter(code=code)
        if activation_record_results.exists():
            activation_record = activation_record_results[0]
            form.user = activation_record.user
            valid_code = code_is_valid(
                code,
                request.POST.get("email"),
                activation_record.user,
                settings.ACTIVATION_EXPIRATION_DAYS,
            )
            if valid_code and form.is_valid():
                signer = TimestampSigner()
                plain_text_email = signer.unsign(
                    form.cleaned_data["email"] + ":" + activation_record.code
                )
                if (
                    plain_text_email == form.cleaned_data["email"]
                    and plain_text_email == form.user.email
                ):
                    form.user.is_active = True
                    form.save()  # save the activation form (password set)
                    form.user.save()  # save the users is_active flag

                    user = authenticate(
                        request,
                        username=form.user.username,
                        password=form.cleaned_data["new_password1"],
                    )
                    if user and user.is_active:
                        activation_record.delete()  # delete the activation record so it can no longer be used
                        login(request, user)
                        return redirect(auth.index)
        form.add_error(
            None,
            "Error activating account.Please check the link, email, and password entered and make sure they are valid.",
        )
    else:
        form = CustomSetPasswordForm(None)
    return render(request, "authentication/activation.html", {"form": form})


def forgot_password_view(request):
    if request.method == "POST":
        form = ForgotPasswordForm(data=request.POST)
        if form.is_valid():
            results = User.objects.filter(email=form.cleaned_data["email"])
            if results.exists():
                user = results[0]
                signer = TimestampSigner()
                signed_value = signer.sign(user.email)
                code_start_index = signed_value.find(":") + 1
                if len(signed_value) > code_start_index:
                    code = signed_value[code_start_index:]

                    forgot_password_record = ForgotPassword(user=user, code=code)
                    forgot_password_record.save()

                    send_forgot_password_email(request, user)
            # "success" message is shown regardless so malicious users can't query this page for valid emails
            messages.success(
                request,
                "If an account exists with the email address a reset password will be emailed to you. Please check your email and follow instructions from there.",
            )
    else:
        form = ForgotPasswordForm()
    return render(request, "authentication/forgot_password.html", {"form": form})


def reset_password_view(request, code: str):
    if request.method == "POST":
        form = CustomSetPasswordForm(user=None, data=request.POST)
        forgot_password_results = ForgotPassword.objects.filter(code=code)
        if forgot_password_results.exists():
            forgot_password_record = forgot_password_results[0]
            form.user = forgot_password_record.user
            valid_code = code_is_valid(
                code,
                request.POST["email"],
                forgot_password_record.user,
                settings.RESET_PASSWORD_EXPIRATION_DAYS,
            )
            if valid_code and form.is_valid():
                signer = TimestampSigner()
                plain_text_email = signer.unsign(
                    form.cleaned_data["email"] + ":" + forgot_password_record.code
                )
                if (
                    plain_text_email == form.cleaned_data["email"]
                    and plain_text_email == form.user.email
                ):
                    form.save()  # save the forgot password form (password set)

                    form.user.is_active = True
                    user = authenticate(
                        request,
                        username=form.user.username,
                        password=form.cleaned_data["new_password1"],
                    )
                    if user and user.is_active:
                        # delete the forgot password record so it can no longer be used
                        forgot_password_record.delete()
                        login(request, user)
                        return redirect(auth.index)
        form.add_error(
            None,
            "Error resetting the password for this account. Please check the link, email, and password entered and make sure they are valid.",
        )
    else:
        form = CustomSetPasswordForm(None)
    return render(request, "authentication/reset_password.html", {"form": form})


def user_detail(request, pk: int):
    current_user = request.user
    if current_user.pk != pk:
        raise PermissionDenied()
    if request.method == "POST":
        user = get_object_or_404(User, pk=pk)
        f = UserEditSelfForm(request.POST, instance=user)
        if f.is_valid():
            f.save()
            messages.success(request, "User updated successfully")
            # Redirect back to current page with url params
            return redirect(request.build_absolute_uri())
    else:
        user = get_object_or_404(User, pk=pk)
        f = UserEditSelfForm(instance=user)

    return render(request, "sysadmin/user_detail.html", {"form": f})


def logout_view(request):
    logout(request)
    return redirect(auth.index)


def code_is_valid(code: str, email: str, user: User, max_days: int):
    max_seconds = max_days * 24 * 60 * 60

    signer = TimestampSigner()
    try:
        signed_text = signer.unsign(email + ":" + code, max_age=max_seconds)
        return signed_text == email
    except:
        return False


def send_forgot_password_email(request, user: User):
    plaintext = get_template("authentication/forgot_password_email.txt")
    html = get_template("authentication/forgot_password_email.html")

    url = request.build_absolute_uri(
        reverse("authentication:reset-password", args=(user.forgotpassword.code,))
    )
    expiration_date = date.today() + timedelta(
        days=settings.RESET_PASSWORD_EXPIRATION_DAYS
    )
    context = {"user": user, "url": url, "expiration_date": expiration_date}

    subject, from_email, to = "PAS Profile Created", "pas@email.com", user.email
    text_content = plaintext.render(context)
    html_content = html.render(context)

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)
