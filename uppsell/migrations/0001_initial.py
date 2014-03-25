# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Customer'
        db.create_table('customers', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('first_name', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=30, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=30, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(db_index=True, max_length=75, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_logged_in_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'uppsell', ['Customer'])

        # Adding model 'Address'
        db.create_table('addresses', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['uppsell.Customer'])),
            ('line1', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('line2', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('line3', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('zip', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('province', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('country_code', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('other', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_used', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'uppsell', ['Address'])

        # Adding model 'LinkedAccountType'
        db.create_table('linked_account_types', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal(u'uppsell', ['LinkedAccountType'])

        # Adding model 'LinkedAccount'
        db.create_table('linked_accounts', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['uppsell.LinkedAccountType'])),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['uppsell.Customer'])),
            ('provider', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('account_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('linked_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'uppsell', ['LinkedAccount'])

        # Adding model 'Store'
        db.create_table('stores', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('default_lang', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('default_currency', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('sales_tax_rate', self.gf('django.db.models.fields.FloatField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'uppsell', ['Store'])

        # Adding model 'ProductGroup'
        db.create_table('product_groups', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'uppsell', ['ProductGroup'])

        # Adding model 'Product'
        db.create_table('products', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['uppsell.ProductGroup'])),
            ('sku', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('subtitle', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=10000)),
            ('stock_units', self.gf('django.db.models.fields.FloatField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'uppsell', ['Product'])

        # Adding model 'ProductCode'
        db.create_table('product_codes', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['uppsell.ProductGroup'])),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'uppsell', ['ProductCode'])

        # Adding model 'Listing'
        db.create_table('listings', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('store', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['uppsell.Store'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['uppsell.Product'])),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('sales_tax_rate', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('subtitle', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=10000, blank=True)),
        ))
        db.send_create_signal(u'uppsell', ['Listing'])

        # Adding model 'Cart'
        db.create_table('carts', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('store', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['uppsell.Store'])),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['uppsell.Listing'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'uppsell', ['Cart'])

        # Adding model 'CartItem'
        db.create_table('cart_items', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cart', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['uppsell.Cart'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['uppsell.Listing'])),
            ('quantity', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
        ))
        db.send_create_signal(u'uppsell', ['CartItem'])

        # Adding model 'Coupon'
        db.create_table('coupons', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('relation', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('store', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['uppsell.Store'])),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['uppsell.Customer'], null=True, blank=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['uppsell.Listing'], null=True, blank=True)),
            ('product_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['uppsell.ProductGroup'], null=True, blank=True)),
            ('discount_amount', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=2, blank=True)),
            ('discount_pct', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('max_uses', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('remaining', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('valid_from', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('valid_until', self.gf('django.db.models.fields.DateTimeField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'uppsell', ['Coupon'])

        # Adding model 'CouponSpend'
        db.create_table('coupon_spends', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['uppsell.Customer'])),
            ('coupon', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['uppsell.Coupon'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'uppsell', ['CouponSpend'])

        # Adding unique constraint on 'CouponSpend', fields ['customer', 'coupon']
        db.create_unique('coupon_spends', ['customer_id', 'coupon_id'])

        # Adding model 'Order'
        db.create_table('orders', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('store', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['uppsell.Store'])),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['uppsell.Customer'])),
            ('order_state', self.gf('django.db.models.fields.CharField')(default='init', max_length=30)),
            ('payment_state', self.gf('django.db.models.fields.CharField')(default='init', max_length=30)),
            ('fraud_state', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('coupon', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['uppsell.Coupon'], null=True)),
            ('transaction_id', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('shipping_address', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='shipping_address', null=True, to=orm['uppsell.Address'])),
            ('billing_address', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='billing_address', null=True, to=orm['uppsell.Address'])),
            ('order_total', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('order_shipping_total', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('payment_made_ts', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'uppsell', ['Order'])

        # Adding model 'OrderItem'
        db.create_table('order_items', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['uppsell.Order'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['uppsell.Listing'])),
            ('quantity', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
        ))
        db.send_create_signal(u'uppsell', ['OrderItem'])

        # Adding model 'OrderEvent'
        db.create_table('order_events', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['uppsell.Order'])),
            ('action_type', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('event', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('state_before', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('state_after', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=2000, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'uppsell', ['OrderEvent'])

        # Adding model 'Invoice'
        db.create_table('invoices', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order_id', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('store_id', self.gf('django.db.models.fields.IntegerField')()),
            ('product_id', self.gf('django.db.models.fields.IntegerField')()),
            ('psp_id', self.gf('django.db.models.fields.IntegerField')()),
            ('user_jid', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('transaction_id', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('psp_type', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('quantity', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('order_total', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('order_shipping_total', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('user_fullname', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('shipping_address', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('billing_address', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('user_mobile_msisdn', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('user_email', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('psp_response_code', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('psp_response_text', self.gf('django.db.models.fields.CharField')(max_length=10000)),
            ('payment_made_ts', self.gf('django.db.models.fields.DateTimeField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'uppsell', ['Invoice'])


    def backwards(self, orm):
        # Removing unique constraint on 'CouponSpend', fields ['customer', 'coupon']
        db.delete_unique('coupon_spends', ['customer_id', 'coupon_id'])

        # Deleting model 'Customer'
        db.delete_table('customers')

        # Deleting model 'Address'
        db.delete_table('addresses')

        # Deleting model 'LinkedAccountType'
        db.delete_table('linked_account_types')

        # Deleting model 'LinkedAccount'
        db.delete_table('linked_accounts')

        # Deleting model 'Store'
        db.delete_table('stores')

        # Deleting model 'ProductGroup'
        db.delete_table('product_groups')

        # Deleting model 'Product'
        db.delete_table('products')

        # Deleting model 'ProductCode'
        db.delete_table('product_codes')

        # Deleting model 'Listing'
        db.delete_table('listings')

        # Deleting model 'Cart'
        db.delete_table('carts')

        # Deleting model 'CartItem'
        db.delete_table('cart_items')

        # Deleting model 'Coupon'
        db.delete_table('coupons')

        # Deleting model 'CouponSpend'
        db.delete_table('coupon_spends')

        # Deleting model 'Order'
        db.delete_table('orders')

        # Deleting model 'OrderItem'
        db.delete_table('order_items')

        # Deleting model 'OrderEvent'
        db.delete_table('order_events')

        # Deleting model 'Invoice'
        db.delete_table('invoices')


    models = {
        u'uppsell.address': {
            'Meta': {'object_name': 'Address', 'db_table': "'addresses'"},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'country_code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['uppsell.Customer']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_used': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'line1': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'line2': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'line3': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'other': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'uppsell.cart': {
            'Meta': {'object_name': 'Cart', 'db_table': "'carts'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['uppsell.Listing']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['uppsell.Store']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'uppsell.cartitem': {
            'Meta': {'object_name': 'CartItem', 'db_table': "'cart_items'"},
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['uppsell.Cart']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['uppsell.Listing']"}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'})
        },
        u'uppsell.coupon': {
            'Meta': {'object_name': 'Coupon', 'db_table': "'coupons'"},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['uppsell.Customer']", 'null': 'True', 'blank': 'True'}),
            'discount_amount': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'discount_pct': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_uses': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['uppsell.Listing']", 'null': 'True', 'blank': 'True'}),
            'product_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['uppsell.ProductGroup']", 'null': 'True', 'blank': 'True'}),
            'relation': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'remaining': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['uppsell.Store']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'valid_from': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'valid_until': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'uppsell.couponspend': {
            'Meta': {'unique_together': "(('customer', 'coupon'),)", 'object_name': 'CouponSpend', 'db_table': "'coupon_spends'"},
            'coupon': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['uppsell.Coupon']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['uppsell.Customer']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'uppsell.customer': {
            'Meta': {'object_name': 'Customer', 'db_table': "'customers'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'db_index': 'True', 'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '30', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_logged_in_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '30', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'uppsell.invoice': {
            'Meta': {'object_name': 'Invoice', 'db_table': "'invoices'"},
            'billing_address': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'order_shipping_total': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'order_total': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'payment_made_ts': ('django.db.models.fields.DateTimeField', [], {}),
            'product_id': ('django.db.models.fields.IntegerField', [], {}),
            'psp_id': ('django.db.models.fields.IntegerField', [], {}),
            'psp_response_code': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'psp_response_text': ('django.db.models.fields.CharField', [], {'max_length': '10000'}),
            'psp_type': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'shipping_address': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'store_id': ('django.db.models.fields.IntegerField', [], {}),
            'transaction_id': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user_email': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user_fullname': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'user_jid': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user_mobile_msisdn': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'uppsell.linkedaccount': {
            'Meta': {'object_name': 'LinkedAccount', 'db_table': "'linked_accounts'"},
            'account_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['uppsell.Customer']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'linked_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'provider': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['uppsell.LinkedAccountType']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'uppsell.linkedaccounttype': {
            'Meta': {'object_name': 'LinkedAccountType', 'db_table': "'linked_account_types'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        u'uppsell.listing': {
            'Meta': {'object_name': 'Listing', 'db_table': "'listings'"},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '10000', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['uppsell.Product']"}),
            'sales_tax_rate': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['uppsell.Store']"}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'uppsell.order': {
            'Meta': {'object_name': 'Order', 'db_table': "'orders'"},
            'billing_address': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'billing_address'", 'null': 'True', 'to': u"orm['uppsell.Address']"}),
            'coupon': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['uppsell.Coupon']", 'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['uppsell.Customer']"}),
            'fraud_state': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order_shipping_total': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'order_state': ('django.db.models.fields.CharField', [], {'default': "'init'", 'max_length': '30'}),
            'order_total': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'payment_made_ts': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'payment_state': ('django.db.models.fields.CharField', [], {'default': "'init'", 'max_length': '30'}),
            'shipping_address': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'shipping_address'", 'null': 'True', 'to': u"orm['uppsell.Address']"}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['uppsell.Store']"}),
            'transaction_id': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'uppsell.orderevent': {
            'Meta': {'object_name': 'OrderEvent', 'db_table': "'order_events'"},
            'action_type': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['uppsell.Order']"}),
            'state_after': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'state_before': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'uppsell.orderitem': {
            'Meta': {'object_name': 'OrderItem', 'db_table': "'order_items'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['uppsell.Order']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['uppsell.Listing']"}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'})
        },
        u'uppsell.product': {
            'Meta': {'object_name': 'Product', 'db_table': "'products'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '10000'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['uppsell.ProductGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'sku': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'stock_units': ('django.db.models.fields.FloatField', [], {}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'uppsell.productcode': {
            'Meta': {'object_name': 'ProductCode', 'db_table': "'product_codes'"},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['uppsell.ProductGroup']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'uppsell.productgroup': {
            'Meta': {'object_name': 'ProductGroup', 'db_table': "'product_groups'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'uppsell.store': {
            'Meta': {'object_name': 'Store', 'db_table': "'stores'"},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'default_currency': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'default_lang': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'sales_tax_rate': ('django.db.models.fields.FloatField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['uppsell']