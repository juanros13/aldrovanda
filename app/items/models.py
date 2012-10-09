from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from shops.models import Shop, ShopSeccion
from hierarchy.models import Category
from easy_thumbnails.files import get_thumbnailer

class Recipient(models.Model):
  name = models.CharField(max_length=50)
  slug = models.CharField(max_length=50)

  class Meta:
    verbose_name = "Para quien"
    verbose_name_plural = "Para quienes"

  def __unicode__(self):
    return self.name

class Occasion(models.Model):
  name = models.CharField(max_length=50)
  slug = models.CharField(max_length=50)
  class Meta:
    verbose_name = "Ocasion"
    verbose_name_plural = "Ocasiones"

  def __unicode__(self):
    return self.name
class Style(models.Model):
  name = models.CharField(max_length=50)
  slug = models.CharField(max_length=50)
  class Meta:
    verbose_name = "Estilo"
    verbose_name_plural = "Estilos"

  def __unicode__(self):
    return self.name
class Tag(models.Model):
  name = models.CharField(max_length=50)
  class Meta:
    verbose_name = "Tag"
    verbose_name_plural = "Tags"

  def __unicode__(self):
    return self.name
class Material(models.Model):
  name = models.CharField(max_length=50)
  class Meta:
    verbose_name = "Material"
    verbose_name_plural = "Materiales"

  def __unicode__(self):
    return self.name

class Item(models.Model):
  name = models.CharField(
    max_length = 150, 
    verbose_name = 'Nombre'
  )
  description = models.TextField(
    verbose_name ='Descripcion'
  )
  stock = models.IntegerField(
    verbose_name = 'Items disponibfles',
  )
  price = models.DecimalField(
    max_digits = 10,   
    decimal_places = 2, 
    verbose_name = 'Precio',
  )
  creation_date = models.DateTimeField(
    auto_now_add = True
  )
  max_images = models.IntegerField(
    verbose_name = 'Maximo numero de imagenes por item',
    default = 5
  )
  featured = models.BooleanField(default=False)
  category = models.ForeignKey(Category)
  shopSeccion = models.ForeignKey(ShopSeccion, blank=True, null=True)
  shop= models.ForeignKey(Shop, default = None, blank=False, null=False)
  tag = models.ManyToManyField(Tag, null=True)
  material = models.ManyToManyField(Material, null=True)
  style = models.ManyToManyField(Style, null=True)
  occasion = models.ForeignKey(Occasion, null=True)
  recipient = models.ForeignKey(Recipient, null=True)
  def get_absolute_url(self):
    return "/items/%s/%s/" % (self.id, self.name.replace (" ", "-"))
  def admin_image(self):
    #return '<img src="../../..'+settings.STATIC_URL+'%s"/>' % self.image_set.get(default=True).image
    image_path=self.image_set.get(default=True).image
    thumbnailer = get_thumbnailer(image_path)
    thumbnail_options = {'crop': True, 'size': (80, 80), 'detail': True, 'upscale':True }
    t=thumbnailer.get_thumbnail(thumbnail_options)
    media_url = settings.MEDIA_URL
    return u'<img src="../../..%s%s" alt="%s" width="80" height="80"/>' % (media_url, t, image_path)
  admin_image.allow_tags = True
  class Meta:
    verbose_name = 'Item'
    verbose_name_plural = "Items"
  def __unicode__(self):
    return self.name

class Image(models.Model):
  item = models.ForeignKey(Item)
  image = models.ImageField(
    upload_to='./uploads/items',
  )
  default = models.BooleanField()
  creation_date = models.DateTimeField(
    auto_now_add = True
  )
  order = models.IntegerField(
    verbose_name = 'Orden de las fotos',
  )
  #sobreescribiendo save para poder hacer unica la imagen default
  def save(self, *args, **kwargs):
    if self.default:
      Image.objects.filter(default=True,item=self.item).update(default=False)
    
    super(Image, self).save(*args, **kwargs)
  class Meta:
    verbose_name = 'Imagen'
    verbose_name_plural = 'Imagenes'

