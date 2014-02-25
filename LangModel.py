
import nltk
import math
import sys

from nltk.corpus import brown

# instantiate with a line like:
# lm = LangModel(3, 0.4, brown.sents())

# this LangModel class is from http://sujitpal.blogspot.com/2013/04/language-model-to-detect-medical.html
class LangModel:
  def __init__(self, order, alpha, sentences):
    self.order = order
    self.alpha = alpha
    if order > 1:
      self.backoff = LangModel(order - 1, alpha, sentences)
      self.lexicon = None
    else:
      self.backoff = None
      self.n = 0
    self.ngramFD = nltk.FreqDist()
    lexicon = set()
    for sentence in sentences:
      # words = nltk.word_tokenize(sentence)
      words = sentence # already tokenized
      wordNGrams = nltk.ngrams(words, order)
      for wordNGram in wordNGrams:
        self.ngramFD.inc(wordNGram)
        if order == 1:
          lexicon.add(wordNGram)
          self.n += 1
    self.v = len(lexicon)

  def logprob(self, ngram):
  	# print 'ngram', ngram,
  	p = self.prob(ngram)
  	# print p
  	return math.log(p)
  
  def prob(self, ngram):
	# print 'ngram', ngram
	if self.backoff != None:
		# if len(ngram) < 2:
		# 	print "error in backoff"
		freq = self.ngramFD[ngram]
		backoffFreq = self.backoff.ngramFD[ngram[1:]]
		if freq == 0:
			return self.alpha * self.backoff.prob(ngram[1:])
		else:
			return float(freq) / float(backoffFreq)
	else:
	# laplace smoothing to handle unknown unigrams
		# print 'ngramFD[ngram]',self.ngramFD[ngram]
		# print self.n, self.v
		return ((self.ngramFD[ngram] + 1.0) / (float(self.n) + float(self.v)))

  def sentenceProbability( self, sentence ):
	words = nltk.word_tokenize(sentence)
	wordTrigrams = nltk.trigrams(words)
	slogprob = 0
	for wordTrigram in wordTrigrams:
	  # print 'trigram: ',wordTrigram
	  logprob = self.logprob(wordTrigram)
	  slogprob += logprob
	sp = slogprob / len(words)
	return sp


def main(argv=None):
    if argv is None:
        argv = sys.argv

	s1 = 'some of protesters who are opposing government threw stones and  bombs of petrol to attack police  who were preventing them from protesting up to building of parliament'
	s2 = 'some of the protesters who are opposing government threw stones and petrol bombs to attack police who were preventing them from protesting at parliament'
	lm = LangModel(3, 0.4, brown.sents())

	# print sentenceProbability( s1.split() )

	print "SENTENCE:", s1
	print "(", lm.sentenceProbability( s1 ) , ")"
	print "SENTENCE:", s2
	print "(", lm.sentenceProbability( s2 ) , ")"


if __name__ == "__main__":
    main()

