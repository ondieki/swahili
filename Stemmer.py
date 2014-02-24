#!/usr/bin/env python

""" Stemming Algorithm
This is the stemming algorithm, 
An algorithm for SWAHILI prefix and suffix stripping, providing you with the core componets of a word in Swahili,
giving you the stem of the word that you query the program with

bavin2009@gmail.com

"""

import sys
import string
import re
from collections import defaultdict

class Stemmer:

    def __init__(self):
        """The main part of the stemming algorithm starts here.
        b is a buffer holding a word to be stemmed. The letters are in b[k0],
        b[k0+1] ... ending at b[k]. In fact k0 = 0 in this demo program. k is
        readjusted downwards as the stemming progresses. Zero termination is
        not in fact used in the algorithm.

        Note that only lower case sequences are stemmed. Forcing to lower case
        should be done before stem(...) is called.
        """

        self.b = ""  # buffer for word to be stemmed
        self.k = 0
        self.k0 = 0
        self.j = 0   # j is a general offset into the string
        self.RESULT = defaultdict(lambda:[])

    def cons(self, i):
        """cons(i) is TRUE <=> b[i] is a consonant."""
        if self.b[i] == 'a' or self.b[i] == 'e' or self.b[i] == 'i' or self.b[i] == 'o' or self.b[i] == 'u':
            return 0
        return 1

    def vowelinstem(self):
        """vowelinstem() is TRUE <=> k0,...j contains a vowel"""
        for i in range(self.k0, self.j + 1):
            if not self.cons(i):
                return 1
        return 0

    def cvc(self, i):
        """cvc(i) is TRUE <=> i-2,i-1,i has the form consonant - vowel - consonant
        and also if the second c is not w,x or y. this is used when trying to
        restore an e at the end of a short  e.g.

           cav(e), lov(e), hop(e), crim(e), but
           snow, box, tray.
        """
        if i < (self.k0 + 2) or not self.cons(i) or self.cons(i-1) or not self.cons(i-2):
            return 0
        ch = self.b[i]
        if ch == 'w' or ch == 'x' or ch == 'y':
            return 0
        return 1

    def starts(self,s):
        """starts(s) is TRUE <=> k0...k starts with string s"""
        if(self.b.find(s, 0, len(s)) != -1):
            return True;
        else:
            return False;

    def ends(self, s):
        """ends(s) is TRUE <=> k0,...k ends with the string s."""
        length = len(s)
        if s[length - 1] != self.b[self.k]: # tiny speed-up
            return 0
        if length > (self.k - self.k0 + 1):
            return 0
        if self.b[self.k-length+1:self.k+1] != s:
            return 0
        self.j = self.k - length
        return 1

    def setto(self, s):
        """setto(s) sets (j+1),...k to the characters in the string s, readjusting k."""
        length = len(s)
        self.b = self.b[:self.j+1] + s + self.b[self.j+length+1:]
        self.k = self.j + length

    def r(self, s):
        """r(s) is used further down."""
        if self.m() > 0:
            self.setto(s)

    def step1ab(self):
        """step1ab() gets rid of plurals and -ed or -ing. e.g.

           walipikia  -> alipik~
           walipikiana ->  walipik
           walichukuliwa -> walichuku
           pikia      ->  pik
           pangiwa    ->  pang 

           #CASES
           pigiliwa
        """


        self.KEY = self.b

        if(len(self.b) > 4 and self.ends("kuwa")):
            J= len(self.b)
            self.b = self.b[0:J]
            self.k = J
        else:
            if self.b[self.k] == 'a':
                if self.ends("eshwa"):
                    self.RESULT[self.KEY].append("made to be")
                    self.k = self.k - 5
                if self.ends("lia"):
                    self.k = self.k - 3
                elif self.ends("liana"):
                    self.RESULT[self.KEY].append("on behalf of each other")
                    self.k = self.k - 5
                elif self.ends("eana") or self.ends("iana"):
                    self.k = self.k - 4
                    self.RESULT[self.KEY].append("at each other")
                elif self.ends("iliwa"):
                    self.k = self.k - 5
                elif self.ends("liwa"):
                    self.k = self.k - 4
                elif self.ends("iwa"):
                    self.k = self.k - 3
                elif self.ends("jika") or self.ends("lika"):
                    self.k = self.k - 3  #hitajika = hitaj, #kamilika = kamil
                elif self.ends("ana"):
                    self.k = self.k - 3
                    self.RESULT[self.KEY].append("each other")
                elif self.ends("ia"):
                    self.k = self.k - 2
                    self.RESULT[self.KEY].append("for")
                elif self.ends("a") and self.cons(self.k - 1):
                    self.k = self.k - 1

                self.b = self.b[0:self.k+1]
            
    def step1c(self):
        """step1c() Get rid of prefix complex Noun+verb, stripping off the propoun,tense,and object, leaving stem and suffix"""
        p = re.compile('(ni|u|a|tu|m|mu|wa|i|li|ya|ki|vi|zi|ku|pa)(li|ta|na)?[a-z]{4}')
        sol = p.match(self.b)
        if(not sol):    #this ones checks to see if word is a verb so we can stem it if it's a verb
            return False
        else: return True;
        

    def STO(self,token, K):

        if token == "kuwa": return "were|will be|was"

        if K == 0:
            #Subject Tokens
            if token == "ku": return "to"
            if token == "wa": return "they"
            if token == "ni": return "me"
            if token == "tu": return "us"
            if token == "mu":  return "you"
            if token == "u" : return "you"
            if token == "a": return "he|she"

        if K == 1:
            #Time Tokens
            if token == "li": return "PT"    #"PT" #PAST TENSE
            if token == "na": return "are"   #PRESENT TENSE
            if token == "ta": return "will"  #FUTURE TENSE
            if token == "ki": return "while" #"PT-CT|PR-CT"
            if token == "mu": return "him|her"


        if K == 2:
            #Object Tokens
            if token == "m": return "him|her"
            if token == "wa": return "them"
            if token == "tu": return "us"
            if token == "ni": return "me"
            if token == "ki": return "it"
    
        #ku,


    def step2(self):
        """step2() checks to see the various prefixes
           #this checks to remove the first tokens that are for the Subject, Verb, Object. 
           #What remains is the root of the verb
        """
        p = re.compile('(ni|u|a|tu|m|wa|i|li|ya|ki|vi|zi|ku|pa)(li|ta|na)(o)?[a-z]{3}')
        p2 = re.compile('(ni|u|a|tu|m|wa|i|li|ya|ki|vi|zi|ku|pa)(li|ta|na)?(ni|tu|ku|mu|wa|cho)?[a-z]{2}')

        #regex 3 = (ni|u|a|tu|m|wa|i|li|ya|ki|vi|zi|ku|pa)(li|ta|na)(ni|tu|ku|mu|wa|cho)?[a-z]{4}

        RESULT = []
        sol = p2.findall(self.b)
        T = map(list,sol)

        if len(T) > 0: 
            L = T[0]

        for t in L:
            if len(t) == 0:
                L.remove(t)

        for i in range(len(L)):
            tok = L[i]
            K = len(tok)
            if self.b == "kuwa": 
                RESULT.append(self.STO(self.b,i))
                break;
            if K > 0:
                RESULT.append(self.STO(tok,i)) #process the subject, tense and object
                self.b = self.b[K:]

        self.RESULT[self.KEY].append(self.b) #store stem in first index
        self.RESULT[self.KEY].append(RESULT) #store result as a list whose key is the original word in sentence


    def step3(self):
        """step3() dels with -ic-, -full, -ness etc. similar strategy to step2."""
        if self.b[self.k] == 'e':
            if self.ends("icate"):     self.r("ic")
            elif self.ends("ative"):   self.r("")
            elif self.ends("alize"):   self.r("al")
        elif self.b[self.k] == 'i':
            if self.ends("iciti"):     self.r("ic")
        elif self.b[self.k] == 'l':
            if self.ends("ical"):      self.r("ic")
            elif self.ends("ful"):     self.r("")
        elif self.b[self.k] == 's':
            if self.ends("ness"):      self.r("")

    def step4(self):
        """step4() takes off -ant, -ence etc., in context <c>vcvc<v>."""
        if self.b[self.k - 1] == 'a':
            if self.ends("al"): pass
            else: return
        elif self.b[self.k - 1] == 'c':
            if self.ends("ance"): pass
            elif self.ends("ence"): pass
            else: return
        elif self.b[self.k - 1] == 'e':
            if self.ends("er"): pass
            else: return
        elif self.b[self.k - 1] == 'i':
            if self.ends("ic"): pass
            else: return
        elif self.b[self.k - 1] == 'l':
            if self.ends("able"): pass
            elif self.ends("ible"): pass
            else: return
        elif self.b[self.k - 1] == 'n':
            if self.ends("ant"): pass
            elif self.ends("ement"): pass
            elif self.ends("ment"): pass
            elif self.ends("ent"): pass
            else: return
        elif self.b[self.k - 1] == 'o':
            if self.ends("ion") and (self.b[self.j] == 's' or self.b[self.j] == 't'): pass
            elif self.ends("ou"): pass
            # takes care of -ous
            else: return
        elif self.b[self.k - 1] == 's':
            if self.ends("ism"): pass
            else: return
        elif self.b[self.k - 1] == 't':
            if self.ends("ate"): pass
            elif self.ends("iti"): pass
            else: return
        elif self.b[self.k - 1] == 'u':
            if self.ends("ous"): pass
            else: return
        elif self.b[self.k - 1] == 'v':
            if self.ends("ive"): pass
            else: return
        elif self.b[self.k - 1] == 'z':
            if self.ends("ize"): pass
            else: return
        else:
            return
        if self.m() > 1:
            self.k = self.j

    def step5(self):
        """step5() removes a final -e if m() > 1, and changes -ll to -l if
        m() > 1.
        """
        print self.b
       
    def stem(self, p, i=None, j=None):
        """In stem(p,i,j), p is a char pointer, and the string to be stemmed
        is from p[i] to p[j] inclusive. Typically i is zero and j is the
        offset to the last character of a string, (p[j+1] == '\0'). The
        stemmer adjusts the characters p[i] ... p[j] and returns the new
        end-point of the string, k. Stemming never increases word length, so
        i <= k <= j. To turn the stemmer into a module, declare 'stem' as
        extern, and delete the remainder of this file.
        """
        if i is None:
            i = 0
        if j is None:
            j = len(p) - 1
        # copy the parameters into statics
        self.b = p
        self.k = j
        self.k0 = i
        if self.k <= self.k0 + 1:
            return self.b 

        K = 0
        
        if(self.step1c()):
            K = 1
            self.step1ab() #only stem the verb form words rather than nouns
       
        #If complex V+N, stem the prefix in order to parse the complex verb+Noun
        if(K): 
            self.step2()

        #self.step3()
        #self.step4()
        #self.step5()
        print dict(self.RESULT)
        return self.b[self.k0:self.k+1]


if __name__ == '__main__':
    p = Stemmer()
    if len(sys.argv) > 1:
        for f in sys.argv[1:]:
            infile = open(f, 'r')
            while 1:
                output = ''
                word = ''
                line = infile.readline()
                if line == '':
                    break
                print "^^^^^^^^^^^^^^^",line
                for c in line:
                    if c.isalpha():
                        word += c.lower()
                    else:
                        if word:
                            output += p.stem(word, 0,len(word)-1)
                            word = ''
                        output += c.lower()
                print output,
            infile.close()
