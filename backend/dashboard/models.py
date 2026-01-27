from django.db import models
from django.utils import timezone


class DashboardCache(models.Model):
    cache_key = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Clé de cache"
    )
    data = models.JSONField(
        verbose_name="Données en cache"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Créé le"
    )
    expires_at = models.DateTimeField(
        verbose_name="Expire le"
    )
    
    class Meta:
        verbose_name = "Cache Dashboard"
        verbose_name_plural = "Caches Dashboard"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.cache_key} - Expire: {self.expires_at.strftime('%Y-%m-%d %H:%M')}"
    
    @classmethod
    def get_cached(cls, key):
        try:
            cache = cls.objects.get(
                cache_key=key,
                expires_at__gt=timezone.now()
            )
            return cache.data
        except cls.DoesNotExist:
            return None
    
    @classmethod
    def set_cached(cls, key, data, minutes=15):
        expires_at = timezone.now() + timezone.timedelta(minutes=minutes)
        cls.objects.update_or_create(
            cache_key=key,
            defaults={'data': data, 'expires_at': expires_at}
        )