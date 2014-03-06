from django.db import models
from datetime import datetime
from time import strftime


# Stolen from http://ianrolfe.livejournal.com/36017.html (read the comments)
class UnixTimestampField(models.DateTimeField):
    """UnixTimestampField: creates a DateTimeField that is represented on the
    database as a TIMESTAMP field rather than the usual DATETIME field.
    """
    def __init__(self, null=False, blank=False, **kwargs):
        super(UnixTimestampField, self).__init__(**kwargs)
        # default for TIMESTAMP is NOT NULL unlike most fields, so we have to
        # cheat a little:
        self.blank, self.isnull = blank, null
        self.null = True # To prevent the framework from shoving in "not null".
        
    def db_type(self, connection):
        typ=['TIMESTAMP']
        # See above!
        if self.isnull:
            typ += ['NULL']
        if self.auto_created:
            typ += ['default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP']
        return ' '.join(typ)
    
    def to_python(self, value):
        if isinstance(value, datetime):
            return value
        return datetime.fromtimestamp(value)
    
    def get_db_prep_value(self, value, connection, prepared=False):
        if value==None:
            return None
        return strftime('%Y%m%d%H%M%S',value.timetuple())

#class AutoPositiveSmallIntegerField(models.AutoField):
#    """AutoPositiveSmallIntegerField: to create a SMALLINT PRIMARY KEY"""
#    
#    def __init__(self, *args, **kwargs):
#        models.AutoField.__init__(self, *args, **kwargs)
#    
#    def get_internal_type(self):
#        return "PositiveSmallIntegerField"
#
## Monkey-patch mysql DatabaseCreation to add the field type
#from django.db.backends.mysql.creation import DatabaseCreation
#DatabaseCreation.data_types["AutoPositiveSmallIntegerField"] = "smallint AUTO_INCREMENT"

