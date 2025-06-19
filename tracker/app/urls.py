from django.urls import path

from . import views

urlpatterns = [
	path("", views.home, name="home"),
	path("candidate/<int:user_id>", views.candidate_page, name="candidate_page")
	# path("/search", views.search, name="search_candidate")
]