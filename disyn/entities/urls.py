from django.urls import path
from . import views

urlpatterns = [
        path('', views.landing_page, name='landing_page'),
    path('entities/', views.EntityListView.as_view(), name='entity_list'),
    path('<int:pk>/', views.EntityDetailView.as_view(), name='entity_detail'),
    path('<int:pk>/upvote/', views.upvote_entity, name='upvote_entity'),
    path('apply/', views.ApplicationCreateView.as_view(), name='apply'),
    path('apply/success/', views.application_success, name='application_success'),
    path('analytics/', views.analytics_dashboard, name='analytics_dashboard'),
    path('applications/', views.ApplicationListView.as_view(), name='application_list'),
    path('applications/<int:pk>/', views.ApplicationDetailView.as_view(), name='application_detail'),
    path('<int:pk>/recent-upvotes/', views.get_recent_upvotes, name='get_recent_upvotes'),
    path('<int:pk>/visitor-apply/', views.submit_visitor_application, name='submit_visitor_application'),
    path('<int:pk>/visitor-applications/', views.entity_visitor_applications, name='entity_visitor_applications'),
    path('visitor-applications/', views.visitor_applications_list, name='visitor_applications_list'),
path('visitor-applications/<int:pk>/', views.visitor_application_detail, name='visitor_application_detail'),
]