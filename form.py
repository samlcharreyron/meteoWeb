from formencode import Schema, validators
from formencode.validators import Number,Wrapper
from formencode.schema import SimpleFormValidator
from datetime import datetime, timedelta
import re

LATREGEX = "^(-?\d{1,2}(\.\d{1,6})?)$"
LONREGEX = "^(-?\d{1,3}(\.\d{1,6})?)$"

class RequestForm(Schema):

		
	# To implement: validate with regex
	#latitude = validators.Regex(regex=LATREGEX)
	#longitude = validators.Regex(regex=LONREGEX)
	
	latitude 	= validators.UnicodeString(not_empty=True)
	longitude 	= validators.UnicodeString(not_empty=True)
	dateS 		= validators.UnicodeString(not_empty=True)
	dateE 		= validators.UnicodeString(not_empty=True)
	
	
		