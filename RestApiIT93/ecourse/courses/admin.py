from django.contrib import admin
from .models import Category, Course, User, Lesson, Tag
from django.utils.html import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget



class LessonForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseAdmin(admin.ModelAdmin):
    search_fields = ['subject', 'category']
    readonly_fields = ['avatar']

    def avatar(self, course):
        if course:
            return mark_safe(
                '<img src="/static/{url}" width="120" />'.format(url=course.image.name)
            )


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['name', 'created_date']
    list_display = ['id', 'name', 'created_date']

class LessonAdmin(admin.ModelAdmin):
    form = LessonForm


# Register your models here.
admin.site.register(User)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Tag)
