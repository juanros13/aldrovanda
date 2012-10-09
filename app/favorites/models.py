from django.db import models
from django.contrib.auth.models import User
from items.models import Item


class Favorite(models.Model):
  item = models.ForeignKey(Item)
  user = models.ForeignKey(User)
  class Meta:
    unique_together = ('item', 'user',)