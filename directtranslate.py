
import sys
import random
import re
import copy

# load dictionary from dict.txt
dict = {}
POSTAG = {}

print '######USING DICT2 ########'

with open( 'dict2.txt', 'r' ) as df:
	for line in df:
		sl = line.strip() # tolerates lines beginning and ending with whitespace. also strips trailing newline
		if len(sl) > 0:
			elements = sl.split(':')
			POSTAG[elements[0]] = elements[1].split('#')[1]
			dict[ elements[0] ] = elements[1].split('#')[0].split(',')


def wordorder(sentence, untagged):
	#Transform V - N -ADJ to V-ADJ-N
	K = len(sentence)
	print K, "+++++++++++++++++TRANSFORMING#############",sentence
	
	temp = copy.deepcopy(sentence)
	for i in range(K):
		word = sentence[i]
		if word == '[N]':
			j = i + 2
			if j < K: #possible to have an adjective after noun
				if sentence[i+2] == '[ADJ]':
					temp[i-1] = sentence[i+1]
					temp[i] = '[ADJ]'
					temp[i+1] = sentence[i-1]
					temp[i+2] = "[N]"
					sentence = temp
					break;
		elif word == ['ADJ'] and j < K and sentence[i+2] == '[N]':
			print 'TO DO'
			#sys.exit()
			#temp[i-1] = sentence[i+1]
			#temp[i+1] = sentence[i-1]
			#temp[i] = '[N]'
			#sentence = temp;
			#break;
			
	#remove two consecutive prepositions e.g. kutoka katika --> kutoka

	return sentence		
		
# naive direct translation of sentence.txt
with open('sentence.txt', 'r') as sf:
	for line in sf:
		print line
		tokens = re.findall(r'\w+', line.lower())
		#print "TOKENS====",tokens
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
				translated.append("[N]")

		print translated
		reordered = wordorder(translated, tokens)
		print ' '.join(reordered)


