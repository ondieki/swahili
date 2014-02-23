
import sys
import random
import re

# load dictionary from dict.txt
dict = {}
POSTAG = {}

print '#######USING DICT2 #########'

with open( 'dict2.txt', 'r' ) as df:
	for line in df:
		sl = line.strip() # tolerates lines beginning and ending with whitespace. also strips trailing newline
		if len(sl) > 0:
			elements = sl.split(':')
			POSTAG[elements[0]] = elements[1].split('#')[1]
			dict[ elements[0] ] = elements[1].split('#')[0].split(',')
		
# naive direct translation of sentence.txt
with open('sentence.txt', 'r') as sf:
	for line in sf:
		#print line
		tokens = re.findall(r'\w+', line.lower())
		print tokens
		translated = []
		for word in tokens:
			word = word.lower()
			if word in dict:
				translations = dict[word]
				k = len(translations)
				i = random.randint(0, k-1)
				if k > 1: 
					translated.append(translations[i])
				else:
					translated.append( dict[word][0] )
					
				translated.append("["+POSTAG[word]+"]")
			else:
				translated.append( word )
		print ' '.join(translated)






