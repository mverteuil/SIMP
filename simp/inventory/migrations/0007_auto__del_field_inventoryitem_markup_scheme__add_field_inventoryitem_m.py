# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'InventoryItem.markup_scheme'
        db.delete_column('inventory_inventoryitem', 'markup_scheme')

        # Adding field 'InventoryItem.markup_decay'
        db.add_column('inventory_inventoryitem', 'markup_decay',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=2),
                      keep_default=False)

        # Adding field 'InventoryItem.markup_growth'
        db.add_column('inventory_inventoryitem', 'markup_growth',
                      self.gf('django.db.models.fields.FloatField')(default=0.6),
                      keep_default=False)

        # Adding field 'InventoryItem.markup_nearest'
        db.add_column('inventory_inventoryitem', 'markup_nearest',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=5),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'InventoryItem.markup_scheme'
        db.add_column('inventory_inventoryitem', 'markup_scheme',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=64, blank=True),
                      keep_default=False)

        # Deleting field 'InventoryItem.markup_decay'
        db.delete_column('inventory_inventoryitem', 'markup_decay')

        # Deleting field 'InventoryItem.markup_growth'
        db.delete_column('inventory_inventoryitem', 'markup_growth')

        # Deleting field 'InventoryItem.markup_nearest'
        db.delete_column('inventory_inventoryitem', 'markup_nearest')


    models = {
        'inventory.account': {
            'Meta': {'object_name': 'Account'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial_balance': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '8', 'decimal_places': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'inventory.inventoryitem': {
            'Meta': {'object_name': 'InventoryItem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'markup_decay': ('django.db.models.fields.PositiveIntegerField', [], {'default': '2'}),
            'markup_growth': ('django.db.models.fields.FloatField', [], {'default': '0.6'}),
            'markup_nearest': ('django.db.models.fields.PositiveIntegerField', [], {'default': '5'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'inventory.purchaser': {
            'Meta': {'object_name': 'Purchaser'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'inventory.transaction': {
            'Meta': {'object_name': 'Transaction'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transactions'", 'null': 'True', 'to': "orm['inventory.Account']"}),
            'delta_balance': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '8', 'decimal_places': '2'}),
            'delta_quantity': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transactions'", 'null': 'True', 'to': "orm['inventory.InventoryItem']"}),
            'purchaser': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'transactions'", 'null': 'True', 'to': "orm['inventory.Purchaser']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['inventory']