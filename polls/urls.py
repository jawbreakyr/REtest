from django.urls import path

from . import views


# set for namespacing 
app_name = 'polls'
urlpatterns = [
	path('', views.index, name='index'),
	path('<int:question_id>/', views.detail, name='details'),
	path('<int:question_id>/results/', views.results, name='results'),
	path('<int:question_id>/votes/', views.vote, name='votes'),
	]