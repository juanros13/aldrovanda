from aldrovanda.models import Product, Image, Category, UserDefault
from django.contrib import admin
from django.forms import ModelForm
from django import forms
from mptt.admin import MPTTModelAdmin

class ImageInline(admin.StackedInline):
	model = Image
	extra = 5

class ProductAdmin(admin.ModelAdmin):
	list_display = ('name', 'stock', 'price', 'creation_date', 'admin_image')
	list_filter = ['creation_date']
	inlines = [ImageInline]

#class CategoryAdmin(CategoryBaseAdmin):
#	pass

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, MPTTModelAdmin)
#admin.site.register(UserDefault)
#admin.site.register(Image)
