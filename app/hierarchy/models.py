from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

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
