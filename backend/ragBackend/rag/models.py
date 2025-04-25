from django.db import models
import uuid


class Document(models.Model):
    """Store metadata about indexed documents"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=512)
    file_type = models.CharField(max_length=50)
    chunk_count = models.IntegerField(default=0)
    indexed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.file_type})"
