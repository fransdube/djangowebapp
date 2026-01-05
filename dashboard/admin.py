from django.contrib import admin
from .models import Task, UserProfile, TaskLog
from .automation import run_email_task, run_scraping_task

class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'user', 'created_at', 'scheduled_time')
    list_filter = ('status', 'user')
    search_fields = ('name', 'description')
    actions = ['run_selected_tasks']

    @admin.action(description='Run selected tasks')
    def run_selected_tasks(self, request, queryset):
        for task in queryset:
            if 'email' in task.name.lower():
                run_email_task(task.pk)
            elif 'scrape' in task.name.lower() or 'scraping' in task.name.lower():
                run_scraping_task(task.pk)
            else:
                task.status = 'completed'
                task.save()
        self.message_user(request, f"{queryset.count()} tasks executed.")

class TaskLogAdmin(admin.ModelAdmin):
    list_display = ('task', 'status', 'timestamp')
    list_filter = ('status', 'timestamp')

admin.site.register(Task, TaskAdmin)
admin.site.register(UserProfile)
admin.site.register(TaskLog, TaskLogAdmin)
