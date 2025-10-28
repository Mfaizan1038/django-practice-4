from django.contrib import admin
from .models import Profile, Project, Task, Document, Comment


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username',)
    actions = ['make_manager', 'make_developer']

    def make_manager(self, request, queryset):
        queryset.update(role='manager')
    make_manager.short_description = "Set selected profiles as Manager"

    def make_developer(self, request, queryset):
        queryset.update(role='developer')
    make_developer.short_description = "Set selected profiles as Developer"


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date')
    list_filter = ('start_date',)
    search_fields = ('title',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'project')
    list_filter = ('status',)
    search_fields = ('title', 'description')


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'version', 'project')
    list_filter = ('project',)
    search_fields = ('name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'task', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('text', 'author__username')
