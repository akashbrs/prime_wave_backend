from django.db import models

class ContactSubmission(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __clstr__(self):
        return f"Submission from {self.name} ({self.email})"

    class Meta:
        ordering = ['-created_at']
