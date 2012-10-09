from django.db import models
from django import forms
from django.contrib.auth.models import User
from easy_thumbnails.files import get_thumbnailer
from aldrovanda.validator import validate_only_numbers, validate_only_letters, validate_only_letters_and_numbers


class Shop(models.Model):
  name = models.CharField(max_length=50, validators=[validate_only_letters_and_numbers], unique=True)
  banner = models.ImageField(
    upload_to = './uploads/banners',
    blank = True
  )
  user = models.ForeignKey(User, default = None, blank=False, null=False)
  def get_absolute_url(self):
    return "/tienda/%s/" % (self.name)
  def __unicode__(self):
    return self.name

  class Meta:
    verbose_name = "Tienda"
    verbose_name_plural = "Tiendas"
    
class ShopForm(forms.ModelForm):
  class Meta:
    model = Shop


class ShopSeccion(models.Model):
  name = models.CharField(max_length=50)
 
  shop = models.ForeignKey(Shop, default = None, blank=False, null=False)
  def get_absolute_url(self):
    return "/tienda/%s/seccion/%s" % (self.shop.name, self.name)
  def __unicode__(self):
    return self.name

  class Meta:
    verbose_name = 'Seccion de la tienda'
    verbose_name_plural = 'Secciones de la tienda'
    
