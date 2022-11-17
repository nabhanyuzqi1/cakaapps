from django.contrib import admin
from .models import *

# Register your models here.
class what_you_learn_TabularInline(admin.TabularInline):
    model = What_you_learn

class Requirements_TabularInline(admin.TabularInline):
    model = Requirements

class who_is_this_course_For_TabularInline(admin.TabularInline):
    model = Who_is_this_course_for

class Video_TabularInline(admin.TabularInline):
    model = Video

class course_admin(admin.ModelAdmin):
    inlines = (what_you_learn_TabularInline, Requirements_TabularInline, who_is_this_course_For_TabularInline, Video_TabularInline)


admin.site.register(Categories)
admin.site.register(Author)
admin.site.register(Course, course_admin)
admin.site.register(Language)
admin.site.register(Level)
admin.site.register(Tag)
admin.site.register(What_you_learn)
admin.site.register(Requirements)
admin.site.register(Who_is_this_course_for)
admin.site.register(Lesson)
admin.site.register(Video)
admin.site.register(Course_type)

admin.site.register(UserCourse)

