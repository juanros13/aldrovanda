from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from items.models import Item
from easy_thumbnails.files import get_thumbnailer

class UserDefault(models.Model):
  # This field is required.
  user = models.OneToOneField(User)
  photo =  models.ImageField(
    upload_to='./uploads/userPhotos',
    blank=True
  )
  country = facebook_id = models.CharField(max_length=50,blank=True)
  state = facebook_id = models.CharField(max_length=50,blank=True)
  city = facebook_id = models.CharField(max_length=50,blank=True)
  # Other fields 
  facebook_id = models.CharField(max_length=300,blank=True)
  facebook_token = models.CharField(max_length=450,blank=True)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserDefault.objects.create(user=instance)
post_save.connect(create_user_profile, sender=User)


