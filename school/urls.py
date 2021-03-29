from django.urls import path

from .views import index

urlpatterns = [
    # School related urls
    path("", index, name="index"),
]
