
from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Course, Lesson, Question, Choice, Submission, Enrollment


class CourseDetailView(generic.DetailView):
    model = Course
    template_name = "onlinecourse/course_details_bootstrap.html"
    context_object_name = "course"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lessons"] = Lesson.objects.filter(
            course=self.object
        ).order_by("order")
        return context


@login_required
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if request.method != "POST":
        return redirect("onlinecourse:course_details", pk=course.id)

    # Find or create the learner's enrollment in this course.
    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user,
        course=course
    )

    # Collect selected choice IDs from the submitted form.
    selected_ids = []

    for key in request.POST:
        if key.startswith("choice"):
            selected_ids.extend(
                int(value)
                for value in request.POST.getlist(key)
                if value.isdigit()
            )

    # Keep only choices belonging to this course.
    choices = Choice.objects.filter(
        id__in=selected_ids,
        question__course=course
    )

    # Create a submission linked to the enrollment.
    submission = Submission.objects.create(
        enrollment=enrollment,
        user=request.user
    )
    submission.choices.set(choices)

    return redirect(
        "onlinecourse:show_exam_result",
        course_id=course.id,
        submission_id=submission.id
    )


@login_required
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)

    submission = get_object_or_404(
        Submission,
        pk=submission_id,
        enrollment__user=request.user,
        enrollment__course=course
    )

    selected_ids = set(
        submission.choices.values_list("id", flat=True)
    )

    total_score = 0
    total_grade = 0
    exam_results = []

    questions = Question.objects.filter(course=course)

    for question in questions:
        is_correct = question.is_get_score(selected_ids)

        total_grade += question.grade

        if is_correct:
            total_score += question.grade

        exam_results.append({
            "question": question,
            "is_correct": is_correct
        })

    percentage = (
        round((total_score / total_grade) * 100, 2)
        if total_grade else 0
    )

    context = {
        "course": course,
        "submission": submission,
        "exam_results": exam_results,
        "selected_ids": selected_ids,
        "total_score": total_score,
        "total_grade": total_grade,
        "percentage": percentage,
    }

    return render(
        request,
        "onlinecourse/exam_result_bootstrap.html",
        context
    )
