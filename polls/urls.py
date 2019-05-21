from django.urls import path

from . import views


# set for namespacing 
app_name = 'polls'
urlpatterns = [
	path('', views.IndexView.as_view(), name='index'),
	path('<int:pk>/', views.DetailView.as_view(), name='details'),
	path('<int:pk>/results/', views.ResultsView.as_view() , name='results'),
	path('<int:question_id>/votes/', views.vote, name='votes'),
	]