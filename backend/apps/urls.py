from django.urls import path
from . import views

urlpatterns = [
    path('psychometricweights/', views.fetch_psychometric_weights, name='psychometricweights-list'),
    path('update_weights/', views.update_weights, name='update_weights'),
    path('create_applicant/', views.create_applicant, name='create_applicant'),
	path('fetch_applicant/', views.fetch_applicants, name='fetch_applicant'),
]
