from django.urls import path

from . import views

urlpatterns = [
    path('foo', views.foo, name='foo'),
    path('rest', views.json_endpoint, name='rest'),
    path('testscore/', views.test_score_form, name='testscore'),
    path('', views.index, name='index'),
]