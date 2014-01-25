#========================================
#|	Base Conversion Tool		|
#|	Author: Robert Cope		|
#|	Date: 	January 2014		|
#|	All Rights Reserved		|
#========================================

__author__ = "Robert Cope"
__license__ = "LGPL, revokable"
__version__ = "0.1"
__maintainer__ = "Robert Cope"
__email__ = "rpcope1@gmail.com"
__status__ = "Alpha"

import string
import sys

possibleValues = list("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")

def convertBase(valueFrom, baseFrom, baseTo, values = possibleValues):
	"""
		convertBase takes a integer and converts from one arbitrary base to another.
		convertBase takes four arguments. The first is the valueFrom, expected to be
		a string. If it is not a string, the function will attempt to 'massage' it into
		a string. This should be something like FF or 10 (a valid value in baseFrom).
		Negative numbers are valid for valueFrom, as long as they are well formatted,
		(i.e. look like -FF). The second argument is baseFrom, which is the int (in decimal) 
		that specifies what base the value is in. The third argument is baseTo, 
		which is the base we want to convert to (also expected to be in decimal, 
		and an int). This will be 'massaged' to int if it is not passed as an int. 
		The final argument is the list (in numerical order) of all possible values,
		set by default to be all decimal integers + all upper case letters. 
		The function will return the value back in the baseTo specified.
	"""
	#First, try to force the baseTo to int, since it may be passed in as a string
	if type(baseTo) is not int:
		baseTo = int(baseTo)
	#Do the same for baseFrom
	if type(baseFrom) is not int:
		baseFrom = int(baseFrom)
	#The baseTo must be less than the values we have, or we'll have big issues.
	assert(baseTo <= len(values)) 
	#As must be baseFrom
	assert(baseFrom <= len(values))
	#Finally, value from should be a string.
	if type(valueFrom) is not str:
		valueFrom = str(valueFrom) 
	#Now, let's strip whitespace from valueFrom, and try to detect if there's a negative sign.
	valueFrom = valueFrom.strip()
	negative = False	
	if valueFrom[0] == '-':
		negative = True
	#Now, remove the negative sign and replace it with just the numerical part.
	valueFrom = valueFrom[1:]	
	try:
		#Convert the value into a machine understandable int.
		tVal = sum([values.index(s)*(baseFrom**i) for i, s in enumerate(list(str(valueFrom)))])
		#Now convert to the new base.
		outputValue = ""
		while tVal:
			outputValue = values[(tVal % (baseTo))] + outputValue
			tVal /= (baseTo)
		if negative:
			outputValue = '-'+outputValue
		return outputValue
	except IndexError:
		raise ValueError, "One or more of the characters passed are not valid in a specified base!"
	except:
		raise
	
def usage(name):
	print name, " converts a number from one base to another."
	print "Usage:", name, "<valueFrom> <baseFrom> <baseTo>"

if __name__ == "__main__":
	if len(sys.argv) == 4:
		print convertBase(*sys.argv[1:])
	else:
		usage(sys.argv[0])
