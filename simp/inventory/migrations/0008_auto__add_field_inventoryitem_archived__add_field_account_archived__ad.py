# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'InventoryItem.archived'
        db.add_column(u'inventory_inventoryitem', 'archived',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Account.archived'
        db.add_column(u'inventory_account', 'archived',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Transaction.archived'
        db.add_column(u'inventory_transaction', 'archived',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Purchaser.archived'
        db.add_column(u'inventory_purchaser', 'archived',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'InventoryItem.archived'
        db.delete_column(u'inventory_inventoryitem', 'archived')

        # Deleting field 'Account.archived'
        db.delete_column(u'inventory_account', 'archived')

        # Deleting field 'Transaction.archived'
        db.delete_column(u'inventory_transaction', 'archived')

        # Deleting field 'Purchaser.archived'
        db.delete_column(u'inventory_purchaser', 'archived')


    models = {
        u'inventory.account': {
            'Meta': {'object_name': 'Account'},
            'archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial_balance': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '8', 'decimal_places': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'inventory.inventoryitem': {
            'Meta': {'object_name': 'InventoryItem'},
            'archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'markup_decay': ('django.db.models.fields.PositiveIntegerField', [], {'default': '2'}),
            'markup_growth': ('django.db.models.fields.FloatField', [], {'default': '1.06'}),
            'markup_nearest': ('django.db.models.fields.PositiveIntegerField', [], {'default': '5'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'inventory.purchaser': {
            'Meta': {'object_name': 'Purchaser'},
            'archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'inventory.transaction': {
            'Meta': {'ordering': "['-timestamp']", 'object_name': 'Transaction'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transactions'", 'null': 'True', 'to': u"orm['inventory.Account']"}),
            'archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'delta_balance': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '8', 'decimal_places': '2'}),
            'delta_quantity': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transactions'", 'null': 'True', 'to': u"orm['inventory.InventoryItem']"}),
            'purchaser': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'transactions'", 'null': 'True', 'to': u"orm['inventory.Purchaser']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['inventory']