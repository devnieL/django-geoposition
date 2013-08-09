from django.db import models

from . import Geoposition
from .forms import GeopositionField as GeopositionFormField
from django.utils.encoding import smart_unicode
from django.db.models import DecimalField
from pprint import pprint

class GeopositionCreator(object):
	def __init__(self, field):
		self.field = field

	def __get__(self,instance,type=None):
		if instance is None:
			return self.field
			raise AttributeError("Can only be accessed via an instance.")
		else:
			return Geoposition(instance.__dict__[self.field.name + "_latitude"],instance.__dict__[self.field.name + "_longitude"])

	def __set__(self,instance,value):
		if isinstance(value, Geoposition):
			setattr(instance, self.position_longitude, value.longitude)
			setattr(instance, self.position_latitude, value.latitude)
		else:
			raise TypeError("%s value mus be a Geoposition instance, not '%r'" % (self.field.name,value))


class GeopositionField(models.Field):
	description = "A geoposition (latitude and longitude)"

	def __init__(self, *args, **kwargs):
		super(GeopositionField, self).__init__(*args, **kwargs)

	def contribute_to_class(self, cls, name):
		self.name = name

		position_longitude = DecimalField(decimal_places=20,max_digits=23,default=0,blank=True)
		cls.add_to_class("%s_longitude" % (self.name,), position_longitude)

		position_latitude = DecimalField(decimal_places=20,max_digits=23,default=0,blank=True)
		cls.add_to_class("%s_latitude" % (self.name,),position_latitude)

		setattr(cls,"%s_longitude" % (self.name,),position_longitude)
		setattr(cls,"%s_latitude" % (self.name,),position_latitude)
		setattr(cls,name,GeopositionCreator(self))
	
	"""def get_internal_type(self):
		return 'CharField'

	def get_db_prep_lookup(self, lookup_type, value):
		pass

	def get_prep_value(self, value):
		return unicode(value)

	def get_db_prep_save(self,value):
		pass
	
	def value_to_string(self, obj):
		value = self._get_val_from_obj(obj)
		return smart_unicode(value)
	
	def formfield(self, **kwargs):
		defaults = {
			'form_class': GeopositionFormField,
		}
		defaults.update(kwargs)
		return super(GeopositionField, self).formfield(**defaults)"""
