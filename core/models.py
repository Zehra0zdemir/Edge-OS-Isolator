from django.db import models

class SystemAuditLog(models.Model):
    """Stores system-level actions performed through the web bridge for accountability."""
    ACTION_CHOICES = [
        ('ADD', 'Tenant Provisioned'),
        ('DELETE', 'Tenant Purged'),
        ('ISOLATE', 'Tenant Isolated (Disabled)'),
        ('ACTIVATE', 'Tenant Activated'),
    ]
    
    timestamp = models.DateTimeField(auto_now_add=True)
    target_username = models.CharField(max_length=150)
    action_type = models.CharField(max_length=10, choices=ACTION_CHOICES)
    status = models.CharField(max_length=20, default='SUCCESS')
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"[{self.timestamp}] {self.action_type} on {self.target_username} - {self.status}"