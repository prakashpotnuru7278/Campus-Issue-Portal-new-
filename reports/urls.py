from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

# Custom LogoutView to allow GET and POST
class CustomLogoutView(LogoutView):
    http_method_names = ['get', 'post']

urlpatterns = [
    # Home & general pages
    path('', views.home, name='home'),
    path('news/', views.news_page, name='news_page'),
    path('signup/', views.signup, name='signup'),
    path('choose-login/', views.choose_login_type, name='choose_login'),

    # Student routes
    path('student/login/', views.student_login, name='student_login'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('status/', views.report_status, name='report_status'),
    path('report/', views.report_issue, name='report_issue'),

    # Admin routes
    path('custom-admin-login/', views.custom_admin_login, name='admin_login'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/issues/', views.admin_issues_list, name='admin_issues_list'),
    path('admin/analytics/', views.admin_analytics, name='admin_analytics'),
    path('admin/post-news/', views.post_news, name='post_news'),
    path('admin/news/', views.admin_news_list, name='admin_news_list'),
    path('admin/update-status/<int:issue_id>/', views.update_issue_status, name='update_issue_status'),

    # Issue detail
    path('issue/<int:issue_id>/', views.view_issue_detail, name='view_issue_detail'),

    # Notifications
    path('notification/read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),

    # Logout
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]
