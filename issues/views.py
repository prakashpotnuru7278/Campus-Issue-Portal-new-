from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import Issue
from .forms import IssueForm

def report_issue(request):
    if request.method == 'POST':
        form = IssueForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('issue_list')
    else:
        form = IssueForm()
    return render(request, 'issues/report_issue.html', {'form': form})

def issue_list(request):
    issues = Issue.objects.all().order_by('-reported_at')
    return render(request, 'issues/issue_list.html', {'issues': issues})
