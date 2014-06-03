# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Product.provisioning_codes'
        db.alter_column('products', 'provisioning_codes', self.gf('django.db.models.fields.CharField')(max_length=5000, null=True))

    def backwards(self, orm):

        # Changing field 'Product.provisioning_codes'
        db.alter_column('products', 'provisioning_codes', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

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
            'line2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'line3': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'other': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'uppsell.card': {
            'Meta': {'object_name': 'Card'},
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['uppsell.Customer']"}),
            'expiry': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'holder': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last4': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'network': ('django.db.models.fields.CharField', [], {'default': "'UNKNOWN'", 'max_length': '12'}),
            'pan': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'})
        },
        u'uppsell.cart': {
            'Meta': {'object_name': 'Cart', 'db_table': "'carts'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['uppsell.Customer']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['uppsell.Store']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'uppsell.cartitem': {
            'Meta': {'unique_together': "(('cart', 'product'),)", 'object_name': 'CartItem', 'db_table': "'cart_items'"},
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['uppsell.Cart']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['uppsell.Listing']"}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'})
        },
        u'uppsell.coupon': {
            'Meta': {'object_name': 'Coupon', 'db_table': "'coupons'"},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['uppsell.Customer']", 'null': 'True', 'blank': 'True'}),
            'discount_amount': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_uses': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['uppsell.Product']", 'null': 'True', 'blank': 'True'}),
            'product_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['uppsell.ProductGroup']", 'null': 'True', 'blank': 'True'}),
            'remaining': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['uppsell.Store']", 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'valid_from': ('django.db.models.fields.DateTimeField', [], {}),
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
            'full_name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_logged_in_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '30', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
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
            'description': ('django.db.models.fields.CharField', [], {'max_length': '10000', 'null': 'True', 'blank': 'True'}),
            'features': ('django.db.models.fields.CharField', [], {'max_length': '10000', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '24', 'decimal_places': '12'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['uppsell.Product']"}),
            'shipping': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '24', 'decimal_places': '12'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['uppsell.Store']"}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'tax_rate': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['uppsell.SalesTaxRate']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
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
            'order_state': ('django.db.models.fields.CharField', [], {'default': "'init'", 'max_length': '30'}),
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
            'order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': u"orm['uppsell.Order']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['uppsell.Listing']"}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'})
        },
        u'uppsell.product': {
            'Meta': {'object_name': 'Product', 'db_table': "'products'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '10000'}),
            'features': ('django.db.models.fields.CharField', [], {'max_length': '10000', 'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['uppsell.ProductGroup']"}),
            'has_stock': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'provisioning_codes': ('django.db.models.fields.CharField', [], {'max_length': '5000', 'null': 'True', 'blank': 'True'}),
            'shipping': ('django.db.models.fields.BooleanField', [], {}),
            'sku': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'stock_units': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
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
        u'uppsell.salestaxrate': {
            'Meta': {'object_name': 'SalesTaxRate'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': "'10'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': "'20'"}),
            'rate': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '6', 'decimal_places': '5'}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['uppsell.Store']"})
        },
        u'uppsell.store': {
            'Meta': {'object_name': 'Store', 'db_table': "'stores'"},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'default_currency': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'default_lang': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['uppsell']