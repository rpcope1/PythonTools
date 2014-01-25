#========================================
#|	String Generation Library	|
#|	Author: Robert Cope		|
#|	Date: 	January 2014		|
#|	All Rights Reserved		|
#========================================


"""
	This simple library is used for generating sets of strings (which can be used as keys or values).
	The GenerateRandomString functions can generate a string based on randomly drawing from a character
	set. The GenerateRandomStrings allows strings of variable length set by an arbitrary function to 
	be generated with (hopefully) minimal hassle. The EqualWeightFunction allows each possible string
	to be drawn with equal probability when combined with the GenerateRandomStrings function. Also included
	are NextLexographicalString and PrevLexographicalString, which allow the user to select the next or
	previous lexographically adjacent string to the one provided.
"""

__author__ = "Robert Cope"
__license__ = "LGPL, revokable"
__version__ = "0.1"
__maintainer__ = "Robert Cope"
__email__ = "rpcope1@gmail.com"
__status__ = "Alpha"


import string
import random
import math

allChr = [chr(i) for i in xrange(256)]

def EqualWeightFunction(byte, charSet=allChr):
	"""
		EqualWeightFunction is a function used for making all possible keys with
		equal probability, when used in combination with GenerateRandomStrings.
		EqualWeightFunction takes two arguments. The first is the byte, which is
		the byte we want to evaluate at. The second is the character set being used.
		The function returns (length of character set)^(byte). 

		This is REALLY useful if you wanted to generate a set of keys where each possible
		key has equal probability. Consider that in the case of all keys of length 1, each key
		has a probability of 1/number of possible characters of being drawn. If we go to length
		two, this probability is squared (i.e. it decreases). This function provides the offset
		factor to ensure each possible key is equally likely. Note, this will cause almost all
		of your keys to have length at or very near to their maximum length (as this is most
		probable since the most unique combinations exist at or near there).
	"""		
	return math.pow(len(charSet), byte)


def GenerateRandomString(bytes, charSet=allChr):
	"""
		GenerateRandomString takes two arguments, bytes, which sets the number
		of characters in the string (since in Python 2.7 1 chr <=> 1 byte), and optionally
		the character set to draw from when building the string. The default character set is 
		all valid ASCII characters (0-127), plus the upper half of the byte range (128-255), 
		represented as a character. The function returns a string of length bytes with random
		characters drawn from the optional argument charSet.
	"""
	return "".join([random.choice(charSet) for i in xrange(bytes)])
	

def GenerateRandomStrings(bytesMin, bytesMax, numStrings = 1, charSet = allChr, distFunc = None):
	"""
		GenerateRandomStrings generates a list of strings distributed according to a set function.
		GenerateRandomStrings takes five arguments. The first argument is bytesMin, which is the
		shortest string length permitted (recall 1 byte <=> 1 char in Python 2). The second argument
		is bytesMax, or the longest string length permitted. The third (and optional argument) is 
		the number of strings to return, which by default is 1. The fourth argument is the set
		of all characters to draw from, which by default is all valid python chr characters (0-255).
		The fifth argument is the (one-argument) function to use to weight sampling. The function
		should accept integers in the range [bytesMin, bytesMax]. Note, the function need not
		sum to zero over (bytesMin, bytesMax). It's default value is None, in which case we use a
		uniform distribution (random.randint) from bytesMin to bytesMax inclusive.

		Each character in the string is drawn uniformly at random from the character set. The length is 
		set by distFunc. This works by taking the sum of all possible integers between and including
		bytesMin and bytesMax. We pick a random number between 0 and 1.0, and iterate through bytesMin
		and bytesMax, until distFunc(byte)/sum is less than or equal to our random number. This will
		deliver a discrete distribution according to (shaped like) the function passed.
	"""	
	retList = list()
	if bytesMin < 0 or bytesMax < 0 or bytesMax < bytesMin:
		raise ValueError, "bytesMin and bytesMax must be integers, with bytesMax > bytesMin"	

	if distFunc:
		#Sum over all the values of our function over the given range.
		total = 1.0*sum([distFunc(i) for i in xrange(bytesMin, bytesMax+1)])
		for s in xrange(numStrings):	
			#cp is the accumulated probability, rp is the randomly set probability target.
			#This algorithm works by setting a probability target, and iterating through
			#the probabilities set by the distribution function until we hit said target.			
			cp = 0
			rp = random.random()
			length = 0			
			for i in xrange(bytesMin, bytesMax+1):
				cp += distFunc(i)/total
				if rp <= cp:
					length = i
					break				
			#If we didn't set a length, our function must be really broken (or went negative somewhere).	
			if not length:
				assert False, "Should never get here! Bad function passed?"
			retList.append(GenerateRandomString(length, charSet))
	else:
		for s in xrange(numStrings):
			retList.append(GenerateRandomString(random.randint(bytesMin,bytesMax), charSet))
	return retList

def NextLexographicalString(s, bytesMin, bytesMax, charSet = allChr):
	"""
		NextLexographicalString provides the lexographically adjacent next string within the bounds
		bytesMin and bytesMax for the string s. The function takes four arguments. The first is
		the string s to find it's adjacent. The second argument is the minimum number of bytes
		for the return string. The third argument is the maximum number of bytes for the return
		string. The four (optional) argument is the character set which we are drawing strings
		from. The default is all byte-code characters (0-255) supported by Python 2. 
	
		Note:
		The function will raise ValueError if you've either passed a string with a length out of
		the bounds of bytesMin and bytesMax, or if the next string would exceed the bytesMax limit.		

	"""
	sortedSet = sorted(charSet)
        retval = list(s)
	length = len(s)
	if length < bytesMin or length > bytesMax:
		raise ValueError
	if length != bytesMax:
		return s + min(charSet)
	else:
		success = False
		for i in xrange(bytesMax-1, bytesMin-2, -1):
			if retval[i] != max(sortedSet):
				retval[i] = sortedSet[sortedSet.index(retval[i])+1]
				success = True
				break 
			else:
				retval[i] = ''
		if not success:
			raise ValueError, "At maximum allowed string!"
		else:
			return "".join(retval)

def PrevLexographicalString(s, bytesMin, bytesMax, charSet = allChr):
	"""
		PrevLexographicalString provides the lexographically adjacent previous string within the bounds
		bytesMin and bytesMax for the string s. The function takes four arguments. The first is
		the string s to find it's adjacent. The second argument is the minimum number of bytes
		for the return string. The third argument is the maximum number of bytes for the return
		string. The four (optional) argument is the character set which we are drawing strings
		from. The default is all byte-code characters (0-255) supported by Python 2. 
	
		Note:
		The function will raise ValueError if you've either passed a string with a length out of
		the bounds of bytesMin and bytesMax, or if the previous string would be lower than the bytesMin limit.
	"""
	sortedSet = sorted(charSet)
	retval = list(s)
	length = len(s)
	if length < bytesMin or length > bytesMax:
		raise ValueError	
	if length == bytesMin and min(charSet)*bytesMin == s:
		raise ValueError, "At minimum allowed string!"
	if length != bytesMax:
		retval[length-1] = sortedSet[sortedSet.index(retval[length-1])-1]
		retval += [max(sortedSet) for i in xrange(length-1, bytesMax-1)]
		return "".join(retval)	
	else:
		for i in xrange(bytesMax-1, bytesMin-2, -1):
			if retval[i] != min(sortedSet):
				retval[i] = sortedSet[sortedSet.index(retval[i])-1]
				break 
			else:
				retval[i] = ''
				break
		return "".join(retval)

#Example usage for uniform probability on all keys....
if __name__ == "__main__":
	random.seed()
	#Build a test set with just ascii letters (so the strings display nicely).
	testSet = string.ascii_letters
	#Build a some random strings.
	print "Testing random string generation functions."
	testStrings = GenerateRandomStrings(10, 32, numStrings = 10, charSet = testSet, distFunc = lambda x: EqualWeightFunction(x, charSet=testSet))
	for i, s in enumerate(testStrings):
		print "String", i, ":"
		print s
		print "Length:", len(s)
	
	print "\n===========================\n"
	print "Now testing lexographical ordering functions."
	c = string.ascii_lowercase
	print "Forward:"	
	ts1 = 'aa'
	for a in xrange(30):	
		print ts1
		ts1 = NextLexographicalString(ts1, 2, 3, charSet= c)
	print "\nReverse:"	
	for a in xrange(30):
		print ts1
		ts1 = PrevLexographicalString(ts1, 2, 3, charSet= c)
	print ts1
	
		
