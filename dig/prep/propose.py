import enchant
from nltk.metrics import edit_distance
import nltk.data
import mysql.connector
import re
import sys

# def replace(self, word):
#     if self.spell_dict.check(word):
#         return word
#     suggestions = self.spell_dict.suggest(word)

#     if suggestions and edit_distance(word, suggestions[0]) <= self.max_dist:
#         return suggestions[0]
#     else:
#         return word

    

def textsFromDB(limit):
    cnx = mysql.connector.connect(user='sqluser', 
                                  password='sqlpassword',
                                  host='localhost',
                                  database='memex_ht')
    cursor = cnx.cursor()

    query = ("""SELECT text from ads limit %s""")
    cursor.execute(query, [limit])

    texts = []
    for (text) in cursor:
        texts.append(text[0])
    cnx.close()
    return texts


sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

def short_words_count(sentence):
    if isinstance(sentence, basestring):
        sentence = nltk.word_tokenize(sentence.strip())
    count = 0
    for token in sentence:
        if len(token) == 1 and token.upper() not in ['A','I'] and token.isalpha():
            count += 1
    return count

def unicode_character_count(sentence):
    count = 0
    for char in sentence:
        if ord(char)>=255:
                count += 1
    return count

def midword_capitalization_count(sentence):
    if isinstance(sentence, basestring):
        sentence = nltk.word_tokenize(sentence.strip())
    count = 0
    for token in sentence:
        for m in re.findall("[a-z][A-Z]", token):
            count += 1
    return count

def midword_digit_count(sentence):
    if isinstance(sentence, basestring):
        sentence = nltk.word_tokenize(sentence.strip())
    count = 0
    for token in sentence:
        for m in re.findall("[a-zA-Z][0-9]", token):
            count += 1
        for m in re.findall("[0-9][a-zA-Z]", token):
            count += 1
    return count    

def propose(limit):
    sc = SpellingCorrector()
    with open('/tmp/report.txt', 'w') as f:
        for text in textsFromDB(limit):
            sentences = sent_detector.tokenize(text.strip())
            for sentence in sentences:
                report(sentence, sc, outstream=f)

def report(sentence, sc=None, outstream=sys.stdout):
    if not sc:
        sc = SpellingCorrector()
    sentence = sentence.replace('\r\n', ' ')
    sentence = sentence.replace('\n', ' ')
    sentence = sentence.replace('\r', ' ')
    sentence = sentence.replace('<BR>', ' ')
    sentence = sentence.replace('<BR/>', ' ')
    sentence = sentence.replace('<br />', ' ')
    sentence = sentence.strip()
    l = len(sentence)
    if l<=100 and l>=20:
        edit = sc.misspell_total_distance(sentence)
        short = short_words_count(sentence)
        uni = unicode_character_count(sentence)
        midcap = midword_capitalization_count(sentence)
        middig = midword_digit_count(sentence)
        score = min(5,edit) + short + uni + midcap + middig
        # print >> outstream, "------"
        # print >> outstream, "Score %s, Len %d, Edit %d, S%d U%d MC%d MD%d:: %s" % (score, l, edit, short, uni, midcap, middig,    sentence.encode('utf-8'))
        print >> outstream, "Score %05d e%-2d+s%-2d+u%-2d+C%-2d+#%-2d %s" % (score, min(5,edit),short,uni,midcap,middig, sentence.encode('utf-8'))

class SpellingCorrector(object):
    def __init__(self, dict_name = 'en_US', max_dist = 10): # en_GB
        self.spell_dict = enchant.Dict(dict_name)
        self.max_dist = max_dist

    def misspell_distance(self, word):
        if self.spell_dict.check(word):
            return 0
        if word.isdigit():
            return 0
        suggestions = self.spell_dict.suggest(word)

        if suggestions:
            # print >> sys.stderr, "%r => %r" % (word, suggestions[0])
            ed = edit_distance(word, suggestions[0])
            if ed:
                return ed
        else:
            return self.max_dist

    def misspell_total_distance(self, sentence):
        sum = 0
        for tok in nltk.word_tokenize(sentence):
            sum += self.misspell_distance(tok)
        return sum

def test_utf8():
    cnx = mysql.connector.connect(user='sqluser', 
                                  password='sqlpassword',
                                  host='localhost',
                                  database='memex_ht')
    cursor = cnx.cursor()
    limit = 2
    query = ("""SELECT substr(text,1,40) from ads where text like %s limit %s""")
    cursor.execute(query, ["%p@ssion@te%", limit])

    texts = []
    for (row) in cursor:
        text = row[0]
        for (j,char) in zip(range(0, len(text)), text):
            print j, char, ord(char);
    cnx.close()
    return texts
