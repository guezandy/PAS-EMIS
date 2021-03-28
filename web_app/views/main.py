from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse

from web_app.models.main import TestScore
from web_app.forms.main import TestScoreForm


def index(request):
    template = loader.get_template("web_app/index.html")
    # Any additional data needed
    context = {}
    return HttpResponse(template.render(context, request))


def foo(request):
    num_test_scores = TestScore.objects.count()
    template = loader.get_template("web_app/foo.html")
    # Any additional data needed
    context = {"num_test_scores": num_test_scores}
    return HttpResponse(template.render(context, request))


def json_endpoint(request):
    return JsonResponse({"num_test_scores": TestScore.objects.count()})


def test_score_form(request):
    num_test_scores = TestScore.objects.count()
    context = {"num_test_scores": num_test_scores}

    print(TestScore.objects.values("sensitive_data"))

    # create object of form
    form = TestScoreForm(request.POST or None)

    # check if form data is valid
    if form.is_valid():
        # save the form data to model
        form.save()

    context["form"] = form
    return render(request, "web_app/foo.html", context)
