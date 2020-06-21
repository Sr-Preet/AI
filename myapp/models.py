from django.db import models

# Create your models here.
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.timezone import now


class Image(models.Model):
    img = models.ImageField(upload_to='image', blank=True, null=True)


@receiver(post_delete, sender=Image)
def submission_delete(sender, instance, **kwargs):
    instance.img.delete(False)


class Chatter(models.Model):
    txt = models.CharField(max_length=100, null=False, blank=False)
    date_added = models.DateTimeField(default=now, null=True)
