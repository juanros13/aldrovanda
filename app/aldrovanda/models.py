from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField
from django.forms import ModelForm
from django.contrib import admin
from django.conf import settings
from easy_thumbnails.files import get_thumbnailer
from categories.models import CategoryBase

class Category(CategoryBase):
   def get_absolute_url(self):
        return str(self.id)
   class Meta:
        verbose_name_plural = 'Categorias'

class Product(models.Model):
	name = models.CharField(
		max_length = 150, 
		verbose_name = 'Nombre'
	)
	description = models.TextField(
		verbose_name ='Descripcion'
	)
	stock = models.IntegerField(
		verbose_name = 'Productos disponibles',
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
		verbose_name = 'Maximo numero de imagenes por producto',
		default = 5
	)
	category = models.ForeignKey(Category)
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
		verbose_name = 'Producto'
		verbose_name_plural = "Productos"
	def __unicode__(self):
		return self.name

class Image(models.Model):
	product = models.ForeignKey(Product)
	image = models.ImageField(
		upload_to='./uploads',
	)
	default = models.BooleanField()
	creation_date = models.DateTimeField(
		auto_now_add = True
	)
	#sobreescribiendo save para poder hacer unica la imagen default
	def save(self, *args, **kwargs):
		if self.default:
			Image.objects.filter(default=True,product=self.product).update(default=False)
		
		super(Image, self).save(*args, **kwargs)
	class Meta:
		verbose_name = 'Imagen'
		verbose_name_plural = 'Imagenes'

