
import sys
import random


# load dictionary from dict.txt
dict = {}

print '#######USING DICT2 #########'

with open( 'dict2.txt', 'r' ) as df:
	for line in df:
		sl = line.strip() # tolerates lines beginning and ending with whitespace. also strips trailing newline
		if len(sl) > 0:
			elements = sl.split(':')
			print elements
			dict[ elements[0] ] = elements[1].split(',')

# naive direct translation of sentence.txt
with open('sentence.txt', 'r') as sf:
	for line in sf:
		print line
		tokens = line.split(' ')
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
				else:translated.append( dict[word][0] )
			else:
				translated.append( word )
		print ' '.join(translated)
		print
