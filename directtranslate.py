
import sys
import random
import re
import copy

from Stemmer import Stemmer

# load dictionary from dict.txt
dict = {}
POSTAG = {}

stem = Stemmer()
stem.DICT = dict



print '######USING DICT2 ########'

with open( 'dict2.txt', 'r' ) as df:
	for line in df:
		sl = line.strip() # tolerates lines beginning and ending with whitespace. also strips trailing newline
		if len(sl) > 0:
			elements = sl.split(':')
			POSTAG[elements[0]] = elements[1].split('#')[1]
			dict[ elements[0] ] = elements[1].split('#')[0].split(',')
	stem.DICT = dict


def wordorder(sentence, swahili):
	#Transform V - N -ADJ to V-ADJ-N
	K = len(sentence)
	#print K, "+++++++++++++++++TRANSFORMING#############",tokens

	temp = copy.deepcopy(sentence)
	for i in range(K):
		word = sentence[i]
		if word == '[V]':# and sentence[i+1] == '[ADV]': #and sentence[i+4] == '[N]':
			s =''
			if len(word.split(',')) == 1: 
				s = stem.input(swahili[i-1])
				#print '####################', s

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
		if word == '[ADJ]' and j < K and sentence[i+2] == '[N]':
			print 'TO DO'
			#swich adjectives and nouns
			#break;
		
			
		#TAKE CARE OF PREPOSITIONAL PHRASES LIKE BAADA YA

			#break;
			#sys.exit()

	#remove two consecutive prepositions e.g. kutoka katika --> kutoka

	return sentence		
		
# naive direct translation of sentence.txt
with open('sentence.txt', 'r') as sf:
	for line in sf:
		print line
		tokens = re.findall(r'\w+', line.lower())
		print "TOKENS ==== ",tokens
		swahili = []
		translated = []
		for i in range(len(tokens) ):
			word = tokens[i].lower()
			if word in dict:
				translations = dict[word]
				k = len(translations)
				i = random.randint(0, k-1)
				if k > 1:
					translated.append(translations[i])
				else:
					translated.append( dict[word][0] )

				translated.append("["+POSTAG[word]+"]")
				
				#swahili copy to use in stemmer
				swahili.append([word])
				swahili.append("["+POSTAG[word]+"]")

			else:
				translated.append(word)
				translated.append("[N]")

				#swahili copy to use in stemmer
				swahili.append(word)
				swahili.append('[N]')

		reordered = wordorder(translated, swahili)
		sent = ' '.join(reordered)
		print '########SENTENCE ########\n', sent



