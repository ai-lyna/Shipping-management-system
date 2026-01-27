from django.db import models

class TypeService(models.Model):
    STANDARD = 'standard'
    EXPRESS = 'express'
    INTERNATIONAL = 'international'

    TYPE_CHOICES = [
        (STANDARD, 'Standard'),
        (EXPRESS, 'Express'),
        (INTERNATIONAL, 'International'),
    ]

    typeService = models.CharField(
        max_length=30,
        choices=TYPE_CHOICES,
        unique=True
    )

    def __str__(self):
        return self.typeService