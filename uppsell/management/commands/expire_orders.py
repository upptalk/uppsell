#-*- coding: utf-8 -*-
"""
@author:        Adam Hayward
@contact:       adam@happy.cat
"""

import logging
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import now
from uppsell.models import Order, OrderEvent
from django.conf import settings

logger = logging.getLogger("console")

class Command(BaseCommand):
    args = ''
    help = 'Expire pending orders'
    timeout = 60 * 60 * 24 # orders expire after 24 hours
    
    def handle(self, *args, **options):
        expire_ts = now() - timedelta(seconds=self.timeout)
        to_expire = Order.objects.filter(order_state="pending_payment",
                updated_at__lt=expire_ts)
        for order in to_expire:
            logger.info("Expiring order %d last updated %s" % (order.id, str(order.updated_at)))
            OrderEvent.objects.create(order=order,
                    action_type = "payment",
                    event = "expire",
                    comment = "Payment expired after %d seconds" % self.timeout)

