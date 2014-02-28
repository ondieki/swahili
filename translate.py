
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
	print 'trained language model not found. training...'
	lm = LangModel(3, 0.4, brown.sents())
	cPickle.dump(lm, open("lm.bin", "wb"))


# print '######USING DICT2 ########'

with open( 'dict2.txt', 'r' ) as df:
	for line in df:
		sl = line.strip() # tolerates lines beginning and ending with whitespace. also strips trailing newline
		if len(sl) > 0:
			elements = sl.split(':')
			word = elements[0].lower()
			POSTAG[ word ] = elements[1].split('#')[1]
			translations = elements[1].split('#')[0].split(',')
			translations = [t.strip() for t in translations]
			# print 'word',word,'translations',translations
			dict[ word ] = translations

	
def swapNounAdjective( sentence ):
	tokens = asTokens( sentence )
	postagged = postag( sentence )


def asTokens( sentence ):
	# Note: I tried the nltk tokenizer (requires the 'punkt' tokenizer model),
	# but it returns the same results, except that the last word retains
	# the end-of-sentence period. So, I think the regex is good.
	# nltk_tokens = nltk.sent_tokenize( line.strip().lower() )
	# print "(NLTK) TOKENS====",nltk_tokens

	tokens = re.findall(r'\w+(?:/\w+)?', sentence )
	# print "TOKENS====",tokens
	return tokens

def asText( tokens ):
	return ' '.join(tokens)

def postag( sentence ):
	tokens = asTokens(sentence)
	for t in tokens:
		if t.lower() not in dict:
			dict[t] = t
			POSTAG[t.lower()] = 'N'
			# print 'adding unknown ',t+'/N', 'to dictionary'

	taggedTokens = [t+'/'+POSTAG[t.lower()] for t in tokens]
	# print 'tagged:',taggedTokens
	return asText(taggedTokens);

def stripTags( sentence ):
	tokens = asTokens(sentence)
	return asText( [re.sub(r'(\w+)/\w+',r'\g<1>',t) for t in tokens] )

# preprocess a swahili sentence
def preprocess( sentence ):
	return sentence.strip()	

def swapNounAdjective( sentence ):
	tokens = asTokens( sentence )
	postagged = postag( sentence )
	patNounAdj = r'(.*)/N\w+(.*?)/ADJ'
	subst = re.sub(patNounAdj, '\g<2>/ADJ \g<1>/N', postagged )
	# print 'subst:', subst
	# print 'stripped: ', stripTags( subst )
	# matchObj = re.match( patnounadj, postagged, re.I)
	# if matchObj:
	# 	print matchObj.groups()
	# else:
	# 	print 'no match ( N then ADJ )'
	return subst

def swapCollapseYa( sentence ):
	tokens = asTokens( sentence )
	postagged = postag( sentence )
	# print 'postagged:',postagged
	patNyaN = r'(\w+)/N\W+ya/PP\W+(\w+)/N'
	subst = re.sub(patNyaN, '\g<2>/N \g<1>/N', postagged )
	# print 'subst:', subst
	# print 'stripped: ', stripTags( subst )
	# matchObj = re.search( patNyaN, postagged, re.I)
	# if matchObj:
	# 	for g in matchObj.groups():
	# 		print g
	# else:
	# 	print 'no match ( /N ya/PP /N )'
	return stripTags( subst )


def lmScoring( sentence ):
	# candidates is the list of candiate sentences formed by trying
	# all possible definitions of all words with >1 translation
	stemmer = Stemmer()
	stemmer.DICT = dict
	candidates = []

	tokens = asTokens( sentence )
	for i in range( len(tokens) ):

		word = tokens[i]

		if word.lower() in dict:

			translations = dict[word.lower()]
			pos = POSTAG[word.lower()]

			# print 'word:',word,', pos:',pos,', dictionary:',translations

			if pos == 'V':
				try:
					stemmer_translations = stemmer.input([word.lower()])
					print 'stemmer returned: ',stemmer_translations
					if stemmer_translations:
						translations = [stemmer_translations]
				except:
					pass
					print 'stemmer threw exception on: ', word.lower()



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

		else:

			# print 'CANDIDATES (',len(candidates),')'
			# print candidates
			# print word, "NOT IN DICTIONARY"
			# words not in dictionary pass through untranslated
			translations = [word]

			old_candidates = candidates[:]
			candidates = []

			if len(old_candidates) == 0:
				candidates.append( [translations[0]] )
			else:
				for c in old_candidates:
					cnew = c + [translations[0]]
					candidates.append( cnew )
			# print 'CANDIDATES (',len(candidates),')'
			# print candidates


	neglobprob = [lm.sentenceProbability( ' '.join(cs) ) for cs in candidates ]
	# print neglobprob
	bestSentence = candidates[ neglobprob.index( min(neglobprob) ) ]
	# print 'CANDIDATES (',len(candidates),')'
	# for c in candidates:
	# 	print ' '.join(c)
	# print 'bestSentence='
	# print ' '.join(bestSentence)
	return ' '.join(bestSentence)


def applyStrategies( sentence ):
	# print '+++REORDERED===='
	# reordered = strategyWordOrder( sentence )
	# sentence = swapNounAdjective( sentence )
	sentence = swapCollapseYa( sentence )
	s = lmScoring( sentence )
	# print '+++Best Score==='
	# print s
	return s

# translation of sentence.txt
def translate(sentenceFile):
	with open(sentenceFile, 'r') as sf:
		for line in sf:
			pline = preprocess( line )
			# print line
			# tokens = re.findall(r'\w+', line.strip().lower())
			# tokens = asTokens( pline )

			print 'Swahili:'
			print pline
			s = applyStrategies( pline )
			print 'English:'
			print s
			print




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
