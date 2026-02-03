from uuid import uuid4
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

STATUS_CHOICES = [
    ('applied', 'Applied'),
    ('scheduled', 'Scheduled'),
    ('rejected', 'Rejected'),
]

class Job(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)

    company = models.CharField(_("Company"), max_length=50)
    role = models.CharField(_("Role"), max_length=50)
    status = models.CharField(_("Staus"), max_length=12,choices=STATUS_CHOICES, default='applied')
    link = models.CharField(_("Link"), max_length=255)
    
    date_applied = models.DateTimeField(_("Applied"), default=timezone.now, editable=False)
    updated_at = models.DateTimeField(_("Updated"), auto_now=True, db_index=True)

    note = models.TextField(_("Note"))

    class Meta:
        ordering = ['company',]

    def __str__(self):
        return self.company

