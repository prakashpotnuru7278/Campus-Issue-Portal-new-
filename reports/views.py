from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import News, Issue, Notification, Category
from .forms import IssueForm, StudentSignupForm, NewsForm


# -----------------------------
# Notifications
# -----------------------------
@login_required
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('student_dashboard')


# -----------------------------
# Signup / Auth
# -----------------------------
class SignUpView(CreateView):
    template_name = 'registration/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')


def signup(request):
    if request.method == 'POST':
        form = StudentSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = StudentSignupForm()
    return render(request, 'registration/signup.html', {'form': form})


def student_login(request):
    return render(request, 'student_login.html')


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            return render(request, 'registration/adminlogin.html', {'error': 'Invalid credentials or not an admin.'})
    return render(request, 'registration/adminlogin.html')


def custom_admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'You do not have admin access.')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'registration/custom_admin_login.html')


# -----------------------------
# Home / News
# -----------------------------
def home(request):
    news_list = News.objects.all().order_by('-created_at')

    notifications = None
    unread_notifications_count = 0
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
        unread_notifications_count = notifications.filter(is_read=False).count()

    context = {
        'news_list': news_list,
        'notifications': notifications,
        'unread_notifications_count': unread_notifications_count,
    }
    return render(request, 'reports/home.html', context)


def news_page(request):
    news_items = News.objects.order_by('-created_at')
    return render(request, 'reports/news_page.html', {'news_items': news_items})


def choose_login_type(request):
    return render(request, 'reports/choose_login.html')


# -----------------------------
# Student Views
# -----------------------------
@login_required
def report_issue(request):
    if request.method == 'POST':
        form = IssueForm(request.POST, request.FILES)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.student = request.user
            issue.save()
            messages.success(request, 'Issue reported successfully.')
            return redirect('report_issue')
    else:
        form = IssueForm()
    return render(request, 'reports/report_issue.html', {'form': form})


@login_required
def report_status(request):
    issues = Issue.objects.filter(student=request.user).order_by('-created_at')
    return render(request, 'reports/report_status.html', {'issues': issues})


@login_required
def student_dashboard(request):
    issues = Issue.objects.filter(student=request.user)
    pending_count = issues.filter(status='Pending').count()
    in_progress_count = issues.filter(status='In Progress').count()
    resolved_count = issues.filter(status='Resolved').count()
    rejected_count = issues.filter(status='Rejected').count()

    context = {
        'total_issues': issues.count(),
        'pending_count': pending_count,
        'in_progress_count': in_progress_count,
        'resolved_count': resolved_count,
        'rejected_count': rejected_count,
    }
    return render(request, 'student_dashboard.html', context)


# -----------------------------
# Admin Views
# -----------------------------
@staff_member_required
def admin_dashboard(request):
    issues = Issue.objects.all()
    news_items = News.objects.order_by('-created_at')
    now = datetime.now()
    greeting = "Morning" if now.hour < 12 else "Afternoon" if now.hour < 18 else "Evening"

    status_counts = Issue.objects.values('status').annotate(count=Count('id'))
    status_dict = {status['status']: status['count'] for status in status_counts}
    pending_count = status_dict.get('Pending', 0)
    resolved_count = status_dict.get('Resolved', 0)
    rejected_count = status_dict.get('Rejected', 0)

    context = {
        'issues': issues,
        'news_items': news_items,
        'total_issues': issues.count(),
        'greeting': greeting,
        'today_date': now.strftime("%A, %d %B"),
        'pending_count': pending_count,
        'resolved_count': resolved_count,
        'rejected_count': rejected_count,
    }
    return render(request, 'reports/admin_dashboard.html', context)


@staff_member_required
def admin_issues_list(request):
    status_filter = request.GET.get('status')
    if status_filter:
        issues = Issue.objects.filter(status=status_filter).order_by('-created_at')
    else:
        issues = Issue.objects.all().order_by('-created_at')

    total_issues = Issue.objects.count()
    pending_count = Issue.objects.filter(status='Pending').count()
    in_progress_count = Issue.objects.filter(status='In Progress').count()
    resolved_count = Issue.objects.filter(status='Resolved').count()
    rejected_count = Issue.objects.filter(status='Rejected').count()

    context = {
        'issues': issues,
        'active_filter': status_filter,
        'total_issues': total_issues,
        'pending_count': pending_count,
        'in_progress_count': in_progress_count,
        'resolved_count': resolved_count,
        'rejected_count': rejected_count,
    }
    return render(request, 'reports/admin_issues_list.html', context)


@require_POST
@staff_member_required
def update_issue_status(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    status = request.POST.get('status')
    issue.status = status
    issue.save()
    return redirect('admin_dashboard')


@staff_member_required
def view_issue_detail(request, issue_id):
    issue = get_object_or_404(Issue.objects.select_related('student'), id=issue_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ["pending", "in_progress", "resolved", "rejected"]:
            issue.status = new_status
            issue.save()
            messages.success(request, "Issue status updated successfully.")
            return redirect('view_issue_detail', issue_id=issue.id)
    return render(request, 'reports/view_issue_detail.html', {'issue': issue})


@staff_member_required
def post_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'News posted successfully.')
            return redirect('admin_dashboard')
    else:
        form = NewsForm()
    return render(request, 'reports/post_news.html', {'form': form})


@staff_member_required
def admin_news_list(request):
    news_items = News.objects.order_by('-created_at')
    return render(request, 'reports/admin_news_list.html', {'news_items': news_items})


@login_required
@staff_member_required
def admin_analytics(request):
    total_issues = Issue.objects.count()
    pending_issues = Issue.objects.filter(status='pending').count()
    in_progress_issues = Issue.objects.filter(status='in_progress').count()
    resolved_issues = Issue.objects.filter(status='resolved').count()
    rejected_issues = Issue.objects.filter(status='rejected').count()

    recent_issues = Issue.objects.select_related('student').order_by('-created_at')[:10]
    issues_over_time = (
        Issue.objects
        .annotate(date=TruncDate('created_at'))
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )

    # Removed categories because there is no Category model
    # categories = Category.objects.annotate(count=Count('issue')).order_by('-count')

    top_reporters = (
        User.objects.annotate(count=Count('issue'))
        .filter(count__gt=0)
        .order_by('-count')[:5]
    )

    context = {
        'total_issues': total_issues,
        'pending_issues': pending_issues,
        'in_progress_issues': in_progress_issues,
        'resolved_issues': resolved_issues,
        'rejected_issues': rejected_issues,
        'recent_issues': recent_issues,
        'issues_over_time': issues_over_time,
        'top_reporters': top_reporters,  # Removed categories
    }

    return render(request, 'reports/admin_analytics.html', context)


