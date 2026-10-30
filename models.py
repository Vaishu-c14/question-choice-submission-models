from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError


class Question(models.Model):
    question_text = models.CharField(max_length=255)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="choices"
    )
    choice_text = models.CharField(max_length=200)
    votes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="submissions"
    )
    choice = models.ForeignKey(
        Choice,
        on_delete=models.CASCADE,
        related_name="submissions"
    )
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="poll_submissions"
    )
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-submitted_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["question", "submitted_by"],
                name="one_submission_per_user_per_question"
            )
        ]

    def clean(self):
        if self.choice_id and self.question_id:
            if self.choice.question_id != self.question_id:
                raise ValidationError(
                    {"choice": "The selected choice must belong to this question."}
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.submitted_by} - {self.question}"
