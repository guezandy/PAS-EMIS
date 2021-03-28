from django.core.paginator import Paginator
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
from sysadmin.forms.user_create import CustomUserCreationForm
from sysadmin.forms.user_detail import CustomEditUserForm
from django.core.mail import send_mail
from django.core.signing import TimestampSigner
from sysadmin.models import Activation

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth.decorators import user_passes_test


@user_passes_test(lambda u: u.is_superuser)
def user_list(request):
    search_term = request.GET.get("search_term")
    page_number = request.GET.get("page")
    number_per_page = 10  # Show 25 contacts per page.

    if search_term is None or search_term == "":
        user_list = User.objects.all()
        search_term = ""

        paginator = Paginator(user_list, number_per_page)
        page_obj = paginator.get_page(page_number)
    else:
        user_list = User.objects.filter(
            Q(username__icontains=search_term)
            | Q(email__icontains=search_term)
            | Q(first_name__icontains=search_term)
            | Q(last_name__icontains=search_term)
        )
        paginator = Paginator(user_list, number_per_page)
        page_obj = paginator.get_page(page_number)

    context = {"user_list": page_obj, "search_term": search_term}
    return render(request, "sysadmin/user_list.html", context)


@user_passes_test(lambda u: u.is_superuser)
def create_user(request):
    if request.method == "POST":
        f = CustomUserCreationForm(request.POST)

        if f.is_valid():
            user = f.save()
            rand_password = User.objects.make_random_password()
            user.set_password(rand_password)
            user.is_active = False
            user.save()

            # create an activation key by signing the user's email
            signer = TimestampSigner()
            signed_value = signer.sign(user.email)
            code = signed_value[signed_value.find(":") + 1 :]

            activation = Activation(user=user, code=code)
            activation.save()

            send_activation_email(request, user)

            messages.success(request, "User created successfully")
            return HttpResponseRedirect(reverse("sysadmin:create-user"))
    else:
        f = CustomUserCreationForm()

    return render(request, "sysadmin/user_create.html", {"form": f})


@user_passes_test(lambda u: u.is_superuser)
def user_detail(request, pk: int):
    if request.method == "POST":
        user = get_object_or_404(User, pk=pk)
        f = CustomEditUserForm(request.POST, instance=user)
        if f.is_valid():
            f.save()
            messages.success(request, "User updated successfully")
            return HttpResponseRedirect(reverse("sysadmin:user-detail", args=(pk,)))
    else:
        user = get_object_or_404(User, pk=pk)
        f = CustomEditUserForm(instance=user)

    return render(request, "sysadmin/user_detail.html", {"form": f})


def send_activation_email(request, user: User):
    plaintext = get_template("sysadmin/user_activation_email.txt")
    html = get_template("sysadmin/user_activation_email.html")

    # url = reverse('web_app:activate', args=(user.activation.code,))
    url = request.build_absolute_uri(
        reverse("web_app:activate", args=(user.activation.code,))
    )
    d = {"user": user, "url": url}

    subject, from_email, to = "PAS Profile Created", "pas@email.com", user.email
    text_content = plaintext.render(d)
    html_content = html.render(d)

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)
