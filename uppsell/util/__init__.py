from email.Utils import formatdate
#from datetime import datetime

def to_rfc2822(dt):
    """Format a timetime or timestamp in RFC 2822 format
    eg 'Sun, 14 Jul 2013 20:14:30 -0000'"""
    try:
        return formatdate(float(dt.strftime('%s')))
    except AttributeError:
        # Wasn't a datetime.datetime() object
        return formatdate(float(dt))

