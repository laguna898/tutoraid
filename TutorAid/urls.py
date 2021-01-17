from django.urls import path

from . import views

app_name = 'TutorAid'
urlpatterns = [
    # ex: /courses/
    path('', views.index, name='index'),
    # ex: /courses/5/
    path('<int:course_id>/', views.detail, name='detail'),
    # ex: /courses/5/results/
    path('<int:course_id>/results/', views.results, name='results'),
    # ex: /courses/5/vote/
    path('<int:course_id>/vote/', views.vote, name='vote'),
]