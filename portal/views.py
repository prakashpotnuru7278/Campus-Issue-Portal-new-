# portal/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import IssueReportForm  # make sure this exists!

def home(request):
    return render(request, 'portal/home.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def report_issue(request):
    if request.method == 'POST':
        form = IssueReportForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'portal/success.html')
    else:
        form = IssueReportForm()
    return render(request, 'portal/report_issue.html', {'form': form})

def issue_submitted(request):
    return render(request, 'portal/submitted.html')


