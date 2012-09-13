from aldrovanda.models import Product, Image, Category, UserDefault, Tag, Shop, Style, Occasion, Recipient, Material
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
admin.site.register(Tag)
admin.site.register(Shop)
admin.site.register(Style)
admin.site.register(Occasion)
admin.site.register(Recipient)
admin.site.register(Material)
#admin.site.register(Image)
