# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'InventoryItem.quantity'
        db.delete_column('inventory_inventoryitem', 'quantity')

        # Adding field 'InventoryItem.initial_quantity'
        db.add_column('inventory_inventoryitem', 'initial_quantity',
                      self.gf('django.db.models.fields.FloatField')(default=0.0),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'InventoryItem.quantity'
        db.add_column('inventory_inventoryitem', 'quantity',
                      self.gf('django.db.models.fields.FloatField')(default=0.0),
                      keep_default=False)

        # Deleting field 'InventoryItem.initial_quantity'
        db.delete_column('inventory_inventoryitem', 'initial_quantity')


    models = {
        'inventory.account': {
            'Meta': {'object_name': 'Account'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial_balance': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '8', 'decimal_places': '2'})
        },
        'inventory.inventoryitem': {
            'Meta': {'object_name': 'InventoryItem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial_quantity': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'markup_scheme': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'inventory.transaction': {
            'Meta': {'object_name': 'Transaction'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transactions'", 'null': 'True', 'to': "orm['inventory.Account']"}),
            'delta_balance': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '8', 'decimal_places': '2'}),
            'delta_quantity': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inbound': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transactions'", 'null': 'True', 'to': "orm['inventory.InventoryItem']"})
        }
    }

    complete_apps = ['inventory']