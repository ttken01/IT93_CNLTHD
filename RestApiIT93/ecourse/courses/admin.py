from django.contrib import admin
from .models import Category, Course, User


class CourseAdmin(admin.ModelAdmin):
    search_fields = ['subject', 'category']


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['name', 'created_date']
    list_display = ['id', 'name', 'created_date']


# Register your models here.
admin.site.register(User)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Course, CourseAdmin)