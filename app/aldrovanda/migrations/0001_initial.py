# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserDefault'
        db.create_table('aldrovanda_userdefault', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('facebook_id', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('facebook_token', self.gf('django.db.models.fields.CharField')(max_length=450)),
        ))
        db.send_create_signal('aldrovanda', ['UserDefault'])

        # Adding model 'Category'
        db.create_table('aldrovanda_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['aldrovanda.Category'])),
            ('full_slug', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('aldrovanda', ['Category'])

        # Adding model 'Recipient'
        db.create_table('aldrovanda_recipient', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('aldrovanda', ['Recipient'])

        # Adding model 'Occasion'
        db.create_table('aldrovanda_occasion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('aldrovanda', ['Occasion'])

        # Adding model 'Style'
        db.create_table('aldrovanda_style', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('aldrovanda', ['Style'])

        # Adding model 'Tag'
        db.create_table('aldrovanda_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('aldrovanda', ['Tag'])

        # Adding model 'Product'
        db.create_table('aldrovanda_product', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('stock', self.gf('django.db.models.fields.IntegerField')()),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('max_images', self.gf('django.db.models.fields.IntegerField')(default=5)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aldrovanda.Category'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['auth.User'])),
            ('style', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aldrovanda.Style'], null=True)),
            ('occasion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aldrovanda.Occasion'], null=True)),
            ('recipient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aldrovanda.Recipient'], null=True)),
        ))
        db.send_create_signal('aldrovanda', ['Product'])

        # Adding M2M table for field tag on 'Product'
        db.create_table('aldrovanda_product_tag', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm['aldrovanda.product'], null=False)),
            ('tag', models.ForeignKey(orm['aldrovanda.tag'], null=False))
        ))
        db.create_unique('aldrovanda_product_tag', ['product_id', 'tag_id'])

        # Adding model 'Shop'
        db.create_table('aldrovanda_shop', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('header', self.gf('django.db.models.fields.TextField')()),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aldrovanda.Product'], null=True)),
        ))
        db.send_create_signal('aldrovanda', ['Shop'])

        # Adding model 'Image'
        db.create_table('aldrovanda_image', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aldrovanda.Product'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('default', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('aldrovanda', ['Image'])

        # Adding model 'Favorite'
        db.create_table('aldrovanda_favorite', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aldrovanda.Product'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('aldrovanda', ['Favorite'])

        # Adding unique constraint on 'Favorite', fields ['product', 'user']
        db.create_unique('aldrovanda_favorite', ['product_id', 'user_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Favorite', fields ['product', 'user']
        db.delete_unique('aldrovanda_favorite', ['product_id', 'user_id'])

        # Deleting model 'UserDefault'
        db.delete_table('aldrovanda_userdefault')

        # Deleting model 'Category'
        db.delete_table('aldrovanda_category')

        # Deleting model 'Recipient'
        db.delete_table('aldrovanda_recipient')

        # Deleting model 'Occasion'
        db.delete_table('aldrovanda_occasion')

        # Deleting model 'Style'
        db.delete_table('aldrovanda_style')

        # Deleting model 'Tag'
        db.delete_table('aldrovanda_tag')

        # Deleting model 'Product'
        db.delete_table('aldrovanda_product')

        # Removing M2M table for field tag on 'Product'
        db.delete_table('aldrovanda_product_tag')

        # Deleting model 'Shop'
        db.delete_table('aldrovanda_shop')

        # Deleting model 'Image'
        db.delete_table('aldrovanda_image')

        # Deleting model 'Favorite'
        db.delete_table('aldrovanda_favorite')


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
        'aldrovanda.occasion': {
            'Meta': {'object_name': 'Occasion'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'aldrovanda.product': {
            'Meta': {'object_name': 'Product'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['aldrovanda.Category']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_images': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'occasion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['aldrovanda.Occasion']", 'null': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['aldrovanda.Recipient']", 'null': 'True'}),
            'stock': ('django.db.models.fields.IntegerField', [], {}),
            'style': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['aldrovanda.Style']", 'null': 'True'}),
            'tag': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['aldrovanda.Tag']", 'null': 'True', 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['auth.User']"})
        },
        'aldrovanda.recipient': {
            'Meta': {'object_name': 'Recipient'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'aldrovanda.shop': {
            'Meta': {'object_name': 'Shop'},
            'header': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['aldrovanda.Product']", 'null': 'True'})
        },
        'aldrovanda.style': {
            'Meta': {'object_name': 'Style'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
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