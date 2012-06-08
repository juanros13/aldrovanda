from aldrovanda.models import Product, Image, Category
from django.contrib import admin
from django.forms import ModelForm
from django import forms
from categories.admin import CategoryBaseAdmin

class ImageInline(admin.StackedInline):
	model = Image
	extra = 5

class ProductAdmin(admin.ModelAdmin):
	list_display = ('name', 'stock', 'price', 'creation_date', 'admin_image')
	list_filter = ['creation_date']
	inlines = [ImageInline]

class CategoryAdmin(CategoryBaseAdmin):
	pass

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
#admin.site.register(Image)
