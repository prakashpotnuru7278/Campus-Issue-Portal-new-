from django.contrib import admin
from .models import Issue, News

class IssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_student', 'status', 'created_at')

    def get_student(self, obj):
        if obj.hide_identity or not obj.student:
            return "Anonymous"
        return obj.student.username
    get_student.short_description = 'Student'

admin.site.register(Issue, IssueAdmin)
admin.site.register(News)
