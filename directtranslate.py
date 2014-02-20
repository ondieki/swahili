

# load dictionary from dict.txt
dict = {}

with open( 'dict.txt', 'r' ) as df:
	for line in df:
		sl = line.strip() # tolerates lines beginning and ending with whitespace. also strips trailing newline
		if len(sl) > 0:
			elements = sl.split(':')
			dict[ elements[0] ] = elements[1]

# naive direct translation of sentence.txt
with open('sentence.txt', 'r') as sf:
	for line in sf:
		print line
		tokens = line.split(' ')
		print tokens
		translated = []
		for word in tokens:
			if word in dict:
				translated.append( dict[word] )
			else:
				translated.append( word )
		print ' '.join(translated)
		print
