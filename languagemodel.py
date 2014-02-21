

dict = {}

unigrams = {}
bigrams = {}
trigrams = {}
fourgrams = {}

with open( 'corpus.txt', 'r' ) as cf:
	for line in cf:
		sl = line.strip() # tolerates lines beginning and ending with whitespace. also strips trailing newline
		if len(sl) > 0: # ignore blank lines
			tokens = line.split(' ')
			for t in tokens:
				if t in unigrams:
					unigrams[t] += 1
				else:
					unigrams[t] = 1
			for tn in range(len(tokens)-1):
				bi = tokens[tn]+' '+tokens[tn+1]
				if bi in bigrams:
					bigrams[bi] += 1
				else:
					bigrams[bi] = 1
			for tn in range(len(tokens)-2):
				tri = tokens[tn]+' '+tokens[tn+1]+' '+tokens[tn+2]
				if tri in trigrams:
					trigrams[tri] += 1
				else:
					trigrams[tri] = 1

print 'unigram count: ',len(unigrams)
print 'bigram count: ',len(bigrams)
print 'trigram count: ',len(trigrams)
print unigrams
# print bigrams
for bi in bigrams:
	if bigrams[bi] > 1:
		print bi,':',bigrams[bi]
# print trigrams
for tri in trigrams:
	if trigrams[tri] > 1:
		print tri,':',trigrams[tri]