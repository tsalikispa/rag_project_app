from django.urls import path
from . import views

urlpatterns = [
    path("query/", views.query_endpoint, name="query"),
    path("upload/", views.upload_document, name="upload_document"),
    path("rebuild-index/", views.rebuild_index, name="rebuild_index"),
]
