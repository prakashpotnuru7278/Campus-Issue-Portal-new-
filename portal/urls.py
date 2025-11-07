# portal/urls.py
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    
      #path('', views.index, name='index'),
    path('', views.home, name='home'),  # This is the homepage view
    # You can add more URLs here later
  
    path('submitted/', views.issue_submitted, name='issue_submitted'),
      path('report/', views.report_issue, name='report_issue'),
      path('signup/', views.signup_view, name='signup'),

     
    #path('submitted/', views.issue_submitted, name='issue_submitted'),
      path('admin/', admin.site.urls),
     # Include your app routes
    path('accounts/', include('django.contrib.auth.urls')),
      
]
