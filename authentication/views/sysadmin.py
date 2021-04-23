from django.core.paginator import Paginator
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
from authentication.forms.sysadmin import (
    AdminUserCreationForm,
    AdminEditUserForm,
    TeacherForm,
    SchoolAdministratorForm,
    PrincipalForm,
    DistrictEducationOfficerForm,
    SchoolSuperviserForm,
    StatisticianAdminForm,
    EvaluationAdminForm,
    SupportServicesAdminForm,
    EarlyChildhoodEducatorForm,
    ExternalAccessorForm,
)
from django.core.mail import send_mail
from django.core.signing import TimestampSigner
from authentication.models.activation import Activation

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth.decorators import user_passes_test
from authentication.models.users import (
    SchoolAdministrator,
    Teacher,
    SchoolPrincipal,
    DistrictEducationOfficer,
    SchoolSuperviser,
    StatisticianAdmin,
    EvaluationAdmin,
    EarlyChildhoodEducator,
    SupportServicesAdmin,
    ExternalAccessor,
    get_user_type,
)
from django.contrib.auth.models import User


form_map = {
    "custom": AdminUserCreationForm,
    "teacher": TeacherForm,
    "school_admin": SchoolAdministratorForm,
    "principal": PrincipalForm,
    "district_officer": DistrictEducationOfficerForm,
    "school_superviser": SchoolSuperviserForm,
    "stat_admin": StatisticianAdminForm,
    "evaluation_admin": EvaluationAdminForm,
    "early_childhood_educator": EarlyChildhoodEducatorForm,
    "support_services_admin": SupportServicesAdminForm,
    "external_accessor": ExternalAccessorForm,
}
user_type_model_map = {
    "custom": User,
    "teacher": Teacher,
    "school_admin": SchoolAdministrator,
    "principal": SchoolPrincipal,
    "district_officer": DistrictEducationOfficer,
    "school_superviser": SchoolSuperviser,
    "stat_admin": StatisticianAdmin,
    "evaluation_admin": EvaluationAdmin,
    "early_childhood_educator": EarlyChildhoodEducator,
    "support_services_admin": SupportServicesAdmin,
    "external_accessor": ExternalAccessor,
}
header_map = {
    "custom": "User",
    "teacher": "Teacher",
    "school_admin": "School Admin",
    "principal": "Principal",
    "district_officer": "District Officer",
    "school_superviser": "School Superviser",
    "stat_admin": "Statistical Admin",
    "evaluation_admin": "Evaluation Admin",
    "early_childhood_educator": "Early childhood educator",
    "support_services_admin": "Support Services Admin",
    "external_accessor": "External Accessor",
}


@user_passes_test(lambda u: u.is_superuser)
def user_list(request):
    search_term = request.GET.get("search_term")
    page_number = request.GET.get("page")
    number_per_page = 10  # Show 25 contacts per page.

    if search_term is None or search_term == "":
        user_list = User.objects.order_by("id")
        search_term = ""

        paginator = Paginator(build_user_values(user_list), number_per_page)
        page_obj = paginator.get_page(page_number)
    else:
        user_list = User.objects.filter(
            Q(username__icontains=search_term)
            | Q(email__icontains=search_term)
            | Q(first_name__icontains=search_term)
            | Q(last_name__icontains=search_term)
        ).order_by("id")
        paginator = Paginator(build_user_values(user_list), number_per_page)
        page_obj = paginator.get_page(page_number)

    context = {"user_list": page_obj, "search_term": search_term}
    return render(request, "sysadmin/user_list.html", context)


def build_user_values(user_list):
    return [
        {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_superuser": user.is_superuser,
            "email": user.email,
            "username": user.username,
            "id": user.id,
            "is_active": user.is_active,
            "type": get_user_type(user),
        }
        for user in user_list
    ]


@user_passes_test(lambda u: u.is_superuser)
def create_user(request, type):

    # Get form based on user type
    Form = form_map.get(type, AdminUserCreationForm)

    if request.method == "POST":
        f = Form(request.POST)

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

            messages.success(
                request,
                "User "
                + user.username
                + " successfully created. An activation email was sent to "
                + user.email
                + ".",
            )
            return HttpResponseRedirect(reverse("authentication:user-directory"))
    else:
        f = Form()

    return render(
        request,
        "sysadmin/user_create.html",
        {"form": f, "header": f"Create {header_map.get(type, 'User')}"},
    )


@user_passes_test(lambda u: u.is_superuser)
def edit_user(request, type, pk):
    Model = user_type_model_map.get(type, User)
    model_query = Model.objects.filter(id=pk)
    if not model_query.exists():
        return redirect("/authentication/sysadmin")

    Form = form_map.get(type, AdminEditUserForm)

    # We have a valid user
    user_instance = model_query.first()
    form = Form(request.POST or None, instance=user_instance)
    if request.method == "POST":
        if form.is_valid():
            new_instance = form.save()
            return HttpResponseRedirect(reverse("authentication:user-directory"))

    return render(
        request,
        "sysadmin/user_create.html",
        {"form": form, "header": f"Edit {header_map.get(type, 'User')}"},
    )


@user_passes_test(lambda u: u.is_superuser)
def user_detail(request, pk: int):
    if request.method == "POST":
        user = get_object_or_404(User, pk=pk)
        f = AdminEditUserForm(request.POST, instance=user)
        if f.is_valid():
            f.save()
            messages.success(request, "User updated successfully")
            return HttpResponseRedirect(
                reverse("authentication:user-detail-admin", args=(pk,))
            )
    else:
        user = get_object_or_404(User, pk=pk)
        f = AdminEditUserForm(instance=user)

    return render(request, "sysadmin/user_detail_admin.html", {"form": f})


def send_activation_email(request, user: User):
    plaintext = get_template("sysadmin/user_activation_email.txt")
    html = get_template("sysadmin/user_activation_email.html")

    url = request.build_absolute_uri(
        reverse("authentication:activate", args=(user.activation.code,))
    )
    d = {"user": user, "url": url}

    subject, from_email, to = "PAS Profile Created", "pas@email.com", user.email
    text_content = plaintext.render(d)
    html_content = html.render(d)

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)

