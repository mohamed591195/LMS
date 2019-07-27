from django.contrib import admin
from courses.models import Subject, Module, Course, Content

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}



class ModuleInline(admin.StackedInline):
    model = Module
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', ]
    list_filter = ['subject']
    date_hierarchy = 'created_at'
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'overview',]
    inlines = [ModuleInline]