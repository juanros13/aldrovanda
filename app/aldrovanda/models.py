from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField
from django.forms import ModelForm
from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings
from easy_thumbnails.files import get_thumbnailer
from mptt.models import MPTTModel, TreeForeignKey


class UserDefault(models.Model):
	# This field is required.
	user = models.OneToOneField(User)

	# Other fields 
	facebook_id = models.CharField(max_length=300)
	facebook_token = models.CharField(max_length=450)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserDefault.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

class Category(MPTTModel):
	name = models.CharField(max_length=200)
	slug = models.SlugField()
	description = models.TextField(blank=True,help_text="Optional")
	parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
	full_slug = models.CharField(max_length=255, blank=True)
	class Meta:
		verbose_name = 'Categoria'
		verbose_name_plural = 'Categorias'
		
	def save(self, *args, **kwargs):
		orig_full_slug = self.full_slug
		if self.parent:
		    self.full_slug = "%s%s/" % (self.parent.full_slug, self.slug)
		else:
		    self.full_slug = "%s/" % self.slug
		obj = super(Category, self).save(*args, **kwargs)
		if orig_full_slug != self.full_slug:
		    for child in self.get_children():
		        child.save()
		return obj
	
	def get_absolute_url(self):
		 return '/categoria/%s' % (self.full_slug)
	def __unicode__(self):
		return self.name

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
	user = models.ForeignKey(User, default = None, blank=False, null=False)
	def get_absolute_url(self):
		return "/productos/%s/" % self.id
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

class Favorite(models.Model):
	product = models.ForeignKey(Product)
	user = models.ForeignKey(User)
	class Meta:
		unique_together = ('product', 'user',)