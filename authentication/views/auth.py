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

from authentication.forms.auth import (
    CustomSetPasswordForm,
    SignUpForm,
    UserEditSelfForm,
    ForgotPasswordForm,
)
from authentication.models.activation import Activation
from authentication.views import auth

from authentication.models.users import Teacher


def index(request):
    if request.user and request.user.is_authenticated:
        return render(request, "base.html", {})
    return render(request, "authentication/index.html", {})


def register_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
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
            username = request.POST["username"]
            password = request.POST["password"]
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
        activation_record = get_object_or_404(Activation, code=code)
        form.user = activation_record.user
        code_is_valid(
            code,
            request.POST["email"],
            activation_record.user,
            settings.ACTIVATION_EXPIRATION_DAYS,
        )
        if form.is_valid():
            try:
                signer = TimestampSigner()
                plain_text_email = signer.unsign(
                    request.POST.get("email") + ":" + activation_record.code
                )
                if (
                    plain_text_email == request.POST.get("email")
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
                else:
                    form.add_error(None, "The code or email provided was invalid.")
            except:
                form.add_error(None, "The code or email provided was invalid.")
    else:
        form = CustomSetPasswordForm(None)
    return render(request, "authentication/activation.html", {"form": form})


def forgot_password_view(request):
    if request.method == "POST":
        form = ForgotPasswordForm(data=request.POST)
        if form.is_valid():
            results = User.objects.filter(email=form.cleaned_data["email"])
            if results:
                user = results[0]
                signer = TimestampSigner()
                signed_value = signer.sign(user.email)
                code = signed_value[signed_value.find(":") + 1 :]

                forgot_password_record = ForgotPassword(user=user, code=code)
                forgot_password_record.save()

                messages.success(
                    request,
                    "If an account exists with the email address a reset password will be emailed to you. Please check your email and follow instructions from there.",
                )

                send_forgot_password_email(request, user)

        else:
            form.add_error("email", "Invalid email address.")
    else:
        form = ForgotPasswordForm()
    return render(request, "authentication/forgot_password.html", {"form": form})


def reset_password_view(request, code: str):
    if request.method == "POST":
        form = CustomSetPasswordForm(user=None, data=request.POST)
        forgot_password_record = get_object_or_404(ForgotPassword, code=code)
        form.user = forgot_password_record.user
        code_is_valid(
            code,
            request.POST["email"],
            forgot_password_record.user,
            settings.RESET_PASSWORD_EXPIRATION_DAYS,
        )
        if form.is_valid():
            try:
                signer = TimestampSigner()
                plain_text_email = signer.unsign(
                    request.POST.get("email") + ":" + forgot_password_record.code
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
                        forgot_password_record.delete()  # delete the forgot password record so it can no longer be used
                        login(request, user)
                        return redirect(auth.index)
                else:
                    form.add_error(None, "The code or email provided was invalid.")
            except:
                form.add_error(None, "The code or email provided was invalid.")
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
    d = {"user": user, "url": url}

    subject, from_email, to = "PAS Profile Created", "pas@email.com", user.email
    text_content = plaintext.render(d)
    html_content = html.render(d)

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)
