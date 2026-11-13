from django.db import models

class Mission(models.Model):
    mission_id = models.CharField(max_length=32, unique=True)
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="COMPLETED")
    checklist_count = models.IntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mission_id} - {self.title}"

    def to_dict(self):
        return {
            "mission_id": self.mission_id,
            "title": self.title,
            "status": self.status,
            "checklist": list(range(self.checklist_count))
        }
