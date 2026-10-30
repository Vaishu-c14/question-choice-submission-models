
from django.contrib import admin
from .models import (
    Course,
    Lesson,
    Question,
    Choice,
    Submission,
    Instructor,
    Learner,
    Enrollment,
)


class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 1


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 2


class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline, QuestionInline]
    list_display = ("name", "pub_date")
    search_fields = ["name", "description"]


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ("question_text", "course", "grade")
    search_fields = ["question_text"]


class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order")
    list_filter = ("course",)


class InstructorAdmin(admin.ModelAdmin):
    list_display = ("user", "full_time", "total_learners")


class LearnerAdmin(admin.ModelAdmin):
    list_display = ("user", "occupation")


class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "date_enrolled", "mode", "rating")


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
admin.site.register(Instructor, InstructorAdmin)
admin.site.register(Learner, LearnerAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
