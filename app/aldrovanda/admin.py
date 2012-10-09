from django.contrib import admin
from django.forms import ModelForm
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from shops.models import ShopForm, Shop, ShopSeccion
from items.models import Item, Image ,Tag, Style, Occasion, Recipient, Material
from users.models import UserDefault
from favorites.models import Favorite
from hierarchy.models import Category
from mptt.admin import MPTTModelAdmin
from feincms.admin import tree_editor

class CategoryAdimin(tree_editor.TreeEditor):
  pass

class ImageInline(admin.StackedInline):
	model = Image
	extra = 5

class ItemAdmin(admin.ModelAdmin):
	list_display = ('name', 'stock', 'price', 'creation_date', 'admin_image')
	list_filter = ['creation_date']
	inlines = [ImageInline]

class ShopAdmin(admin.ModelAdmin):
  model = Shop
  form = ShopForm

#class CategoryAdmin(CategoryBaseAdmin):
#	pass

admin.site.register(Item, ItemAdmin)
admin.site.register(Category, CategoryAdimin)
admin.site.register(Tag)
admin.site.register(Shop, ShopAdmin)
admin.site.register(Style)
admin.site.register(Occasion)
admin.site.register(Recipient)
admin.site.register(Material)
admin.site.register(ShopSeccion)
# Define an inline admin descriptor for UserProfile model
# which acts a bit like a singleton
class UserDefaultInline(admin.StackedInline):
    model = UserDefault
    can_delete = False
    verbose_name_plural = 'profile'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (UserDefaultInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
