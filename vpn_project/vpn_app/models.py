from django.db import models
from django.conf import settings



class VpnServer(models.Model):
    name = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.ip_address})"


class ConnectionLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    vpn_server = models.ForeignKey(VpnServer, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    data_transferred = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    site_visited = models.URLField(null=True, blank=True,max_length=1024)
    external_url = models.URLField()

    def update_data_transferred(self, bytes_transferred):
        self.data_transferred += bytes_transferred
        self.save()

    def duration(self):
        return (self.end_time - self.timestamp) if self.end_time else None

    def __str__(self):
        return f"{self.user.username} connected to {self.vpn_server.name} on {self.timestamp}"


class UserSite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.url}"

