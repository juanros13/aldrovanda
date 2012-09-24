# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ShopSeccion'
        db.create_table('aldrovanda_shopseccion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('shop', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['aldrovanda.Shop'])),
        ))
        db.send_create_signal('aldrovanda', ['ShopSeccion'])


        # Changing field 'Shop.user'
        db.alter_column('aldrovanda_shop', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aldrovanda.UserDefault']))
        # Deleting field 'Product.shop'
        db.delete_column('aldrovanda_product', 'shop_id')

        # Deleting field 'Product.style'
        db.delete_column('aldrovanda_product', 'style_id')

        # Adding field 'Product.shopSeccion'
        db.add_column('aldrovanda_product', 'shopSeccion',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['aldrovanda.ShopSeccion']),
                      keep_default=False)

        # Adding M2M table for field style on 'Product'
        db.create_table('aldrovanda_product_style', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm['aldrovanda.product'], null=False)),
            ('style', models.ForeignKey(orm['aldrovanda.style'], null=False))
        ))
        db.create_unique('aldrovanda_product_style', ['product_id', 'style_id'])


    def backwards(self, orm):
        # Deleting model 'ShopSeccion'
        db.delete_table('aldrovanda_shopseccion')


        # Changing field 'Shop.user'
        db.alter_column('aldrovanda_shop', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))
        # Adding field 'Product.shop'
        db.add_column('aldrovanda_product', 'shop',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['aldrovanda.Shop']),
                      keep_default=False)

        # Adding field 'Product.style'
        db.add_column('aldrovanda_product', 'style',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aldrovanda.Style'], null=True),
                      keep_default=False)

        # Deleting field 'Product.shopSeccion'
        db.delete_column('aldrovanda_product', 'shopSeccion_id')

        # Removing M2M table for field style on 'Product'
        db.delete_table('aldrovanda_product_style')


    models = {
        'aldrovanda.category': {
            'Meta': {'object_name': 'Category'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'full_slug': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['aldrovanda.Category']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'aldrovanda.favorite': {
            'Meta': {'unique_together': "(('product', 'user'),)", 'object_name': 'Favorite'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['aldrovanda.Product']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'aldrovanda.image': {
            'Meta': {'object_name': 'Image'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['aldrovanda.Product']"})
        },
        'aldrovanda.material': {
            'Meta': {'object_name': 'Material'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'aldrovanda.occasion': {
            'Meta': {'object_name': 'Occasion'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'aldrovanda.product': {
            'Meta': {'object_name': 'Product'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['aldrovanda.Category']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'material': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['aldrovanda.Material']", 'null': 'True', 'symmetrical': 'False'}),
            'max_images': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'occasion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['aldrovanda.Occasion']", 'null': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['aldrovanda.Recipient']", 'null': 'True'}),
            'shopSeccion': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['aldrovanda.ShopSeccion']"}),
            'stock': ('django.db.models.fields.IntegerField', [], {}),
            'style': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['aldrovanda.Style']", 'null': 'True', 'symmetrical': 'False'}),
            'tag': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['aldrovanda.Tag']", 'null': 'True', 'symmetrical': 'False'})
        },
        'aldrovanda.recipient': {
            'Meta': {'object_name': 'Recipient'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'aldrovanda.shop': {
            'Meta': {'object_name': 'Shop'},
            'header': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['aldrovanda.UserDefault']"})
        },
        'aldrovanda.shopseccion': {
            'Meta': {'object_name': 'ShopSeccion'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'shop': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['aldrovanda.Shop']"})
        },
        'aldrovanda.style': {
            'Meta': {'object_name': 'Style'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'aldrovanda.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'aldrovanda.userdefault': {
            'Meta': {'object_name': 'UserDefault'},
            'facebook_id': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'facebook_token': ('django.db.models.fields.CharField', [], {'max_length': '450'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['aldrovanda']