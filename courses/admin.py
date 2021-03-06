from django.contrib import admin

# Register your models here.

from models import Course, Lecture,MyCourses
from forms import LectureAdminForm

admin.site.register(MyCourses)

class LectureInline(admin.TabularInline):
    model = Lecture
    form=LectureAdminForm
    prepolated_fields={"slug":('title',)}
    extra=1


class CourseAdmin(admin.ModelAdmin):
    inlines = [LectureInline]
    list_filter = ['updated', 'timestamp']
    list_display = ['title', 'updated', 'timestamp']
    readonly_fields = ['updated', 'timestamp', 'short_title']
    search_fields = ['title', 'description']

    class Meta:
        model = Course

    def short_title(self, obj):
        return obj.title[:3]

admin.site.register(Course, CourseAdmin)