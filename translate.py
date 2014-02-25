
import copy
import cPickle
import getopt
from LangModel import LangModel
import nltk
from nltk.corpus import brown
import random
import re
import sys
from Stemmer import Stemmer

# load dictionary from dict.txt
dict = {}
POSTAG = {}

# load language model
try:
	lm = cPickle.load(open("lm.bin", 'rb'))
except:
	lm = LangModel(3, 0.4, brown.sents())
	cPickle.dump(lm, open("lm.bin", "wb"))


print '######USING DICT2 ########'

with open( 'dict2.txt', 'r' ) as df:
	for line in df:
		sl = line.strip() # tolerates lines beginning and ending with whitespace. also strips trailing newline
		if len(sl) > 0:
			elements = sl.split(':')
			POSTAG[elements[0]] = elements[1].split('#')[1]
			dict[ elements[0] ] = elements[1].split('#')[0].split(',')


def wordorder(sentence, swahili, tokens):
	#Transform V - N -ADJ to V-ADJ-N
	K = len(sentence)
	print K, "+++++++++++++++++TRANSFORMING#############",tokens
	
	#stem = Stemmer

	temp = copy.deepcopy(sentence)
	for i in range(K):
		word = sentence[i]
		j = i + 2
		if word == '[N]':
			if j < K: #possible to have an adjective after noun
				if sentence[i+2] == '[ADJ]':
					temp[i-1] = sentence[i+1]
					temp[i] = '[ADJ]'
					temp[i+1] = sentence[i-1]
					temp[i+2] = "[N]"
					sentence = temp
					break;
		elif word == '[ADJ]' and j < K and sentence[i+2] == '[N]':
			print 'TO DO'
			#swich adjectives and nouns
			#break;
		elif word == '[V]':#and sentence[i+2] == '[ADV]':
			stem = Stemmer()
			if len(word.split(',')) == 1: 
				stem.input(swahili[i-1])
			#temp[i-1] = sentence[i+1]
			#temp[i] = '[ADV]'
			#temp[i+1] = sentence[i-1]
			#temp[i+2] = "[V]"
			#sentence = temp
			#print '####################', sentence
		
		#TAKE CARE OF PREPOSITIONAL PHRASES LIKE BAADA YA

			#break;
			#sys.exit()

	#remove two consecutive prepositions e.g. kutoka katika --> kutoka

	return sentence		
		
# translation of sentence.txt
def translate(sentenceFile):
	with open(sentenceFile, 'r') as sf:
		for line in sf:
			# print line
			tokens = re.findall(r'\w+', line.strip().lower())
			# print "TOKENS====",tokens

			# I tried the nltk tokenizer (requires the 'punkt' tokenizer model),
			# but it returns the same results, except that the last word retains
			# the end-of-sentence period. So, I think the regex is good.
			# nltk_tokens = nltk.sent_tokenize( line.strip().lower() )
			# print "(NLTK) TOKENS====",nltk_tokens

			swahili = []
			translated = []

			# candidates is the list of candiate sentences formed by trying
			# all possible definitions of all words with >1 translation
			candidates = []

			for i in range( len(tokens) ):

				word = tokens[i]

				if word in dict:

					translations = dict[word]
					# print 'word:',word,', translations:',translations

					old_candidates = candidates[:]
					candidates = []
					# print 'old_candidates:', old_candidates

					k = len(translations)
					if k > 1:
						# for idx in range(len(candidates)):
						# 	for t in range(len(translations)):
						if len(old_candidates) == 0:
							for k in range(len(translations)):
								candidates.append( [translations[k]] )
						else:
							for k in range(len(translations)):
								for c in old_candidates:
									# print 'c in old_candidates:',c
									cnew = c + [translations[k]]
									# print cnew
									candidates.append( cnew )
					else:
						# append the current word to all candidate
						# sentences
						if len(old_candidates) == 0:
							candidates.append( [translations[0]] )
						else:
							for c in old_candidates:
								# print 'c in old_candidates:',c
								cnew = c + [translations[0]]
								# print cnew
								candidates.append( cnew )
							# print [c.extend(translations[0]) for c in old_candidates]
							# candidates.extend(  [c.extend(translations[0]) for c in old_candidates] )

					# print 'CANDIDATES (',len(candidates),')'
					# print candidates

					translated.append("["+POSTAG[word]+"]")
					
					#swahili copy to use in stemmer
					swahili.append([word])
					swahili.append("["+POSTAG[word]+"]")

				else:
					print word, "NOT IN DICTIONARY"
					translated.append(word)
					translated.append("[N]")

					#swahili copy to use in stemmer
					swahili.append(word)
					swahili.append('[N]')

			neglobprob = [lm.sentenceProbability( ' '.join(cs) ) for cs in candidates ]
			print neglobprob
			bestSentence = candidates[ neglobprob.index( min(neglobprob) ) ]
			print 'CANDIDATES (',len(candidates),')'
			for c in candidates:
				print ' '.join(c)
			print 'bestSentence='
			print ' '.join(bestSentence)

			print '+++++++++TRANSLATED=======',translated
			reordered = wordorder(translated, swahili,tokens)
			print ' '.join(reordered)



def main(argv=None):
    if argv is None:
        argv = sys.argv

    file = 'sentence-dev.txt'
    if len(argv) == 2:
    	if argv[1] == 'test':
    		file = 'sentence-test.txt'

    translate(file)


if __name__ == "__main__":
    main()
