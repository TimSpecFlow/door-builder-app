from django.db import models


class DoorSpec(models.Model):
    width = models.FloatField(help_text='Width in inches')
    height = models.FloatField(help_text='Height in inches')
    material = models.CharField(max_length=50, default='wood')
    finish = models.CharField(max_length=50, blank=True)
    hardware = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Door {self.width}x{self.height} ({self.material})"
