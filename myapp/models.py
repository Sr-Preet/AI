from django.db import models

# Create your models here.
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Image(models.Model):
    img = models.ImageField(upload_to='image', blank=True, null=True)


@receiver(post_delete, sender=Image)
def submission_delete(sender, instance, **kwargs):
    instance.img.delete(False)
