from django.conf.urls import url, include
import filehash.views as views

urlpatterns = [
    url(r'^', views.main),
]
