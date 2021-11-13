from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):

    user = models.OneToOneField(User, primary_key=True,on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=10, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    GENDER_CHOICES = (
        ('M', 'مرد'),
        ('F', 'زن'),
        ('O', 'هیچکدام'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,default='O')
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


class Address(models.Model):
    userinfo = models.ForeignKey(to = User, on_delete=models.CASCADE,related_name='user_address')
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    address = models.TextField()
