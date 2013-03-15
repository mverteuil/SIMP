# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'InventoryItem'
        db.create_table('inventory_inventoryitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('quantity', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('markup_scheme', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
        ))
        db.send_create_signal('inventory', ['InventoryItem'])

        # Adding model 'Account'
        db.create_table('inventory_account', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('initial_balance', self.gf('django.db.models.fields.DecimalField')(default='0.00', max_digits=8, decimal_places=2)),
        ))
        db.send_create_signal('inventory', ['Account'])

        # Adding model 'Transaction'
        db.create_table('inventory_transaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transactions', null=True, to=orm['inventory.InventoryItem'])),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transactions', null=True, to=orm['inventory.Account'])),
            ('inbound', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('delta_quantity', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('delta_balance', self.gf('django.db.models.fields.DecimalField')(default='0.00', max_digits=8, decimal_places=2)),
        ))
        db.send_create_signal('inventory', ['Transaction'])


    def backwards(self, orm):
        # Deleting model 'InventoryItem'
        db.delete_table('inventory_inventoryitem')

        # Deleting model 'Account'
        db.delete_table('inventory_account')

        # Deleting model 'Transaction'
        db.delete_table('inventory_transaction')


    models = {
        'inventory.account': {
            'Meta': {'object_name': 'Account'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial_balance': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '8', 'decimal_places': '2'})
        },
        'inventory.inventoryitem': {
            'Meta': {'object_name': 'InventoryItem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'markup_scheme': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'quantity': ('django.db.models.fields.FloatField', [], {'default': '0.0'})
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