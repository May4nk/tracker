from django.urls import path

from . import views

urlpatterns = [
	path("", views.home),
	path("create", views.create_candidate),
	path("update/<int:candidate_id>", views.update_candidate),
	path("search/<str:candidate_name>", views.search_candidate),
	path("delete/<int:candidate_id>", views.del_candidate),
	path("get/<int:candidate_id>", views.fetch_candidate)
]