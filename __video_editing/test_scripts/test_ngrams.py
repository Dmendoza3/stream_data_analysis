import nltk
from nltk import bigrams
from nltk import trigrams

text="""LMAOOOO
:grinning_squinting_face: 
:_irysLaugh::_irysLaugh::_irysLaugh:
:_irysLaugh::_irysLaugh::_irysLaugh:
lmao
LOL
rip
lol
:_irysLaugh::_irysLaugh::_irysLaugh:
:_irysLaugh::_irysLaugh::_irysLaugh:
LOL
lmao
great game
:_irysLaugh::_irysLaugh::_irysLaugh:
LMAO
:_irysLaugh: :_irysLaugh: :_irysLaugh: 
RIPBOZO
LMAO
?? lmao
:_irysLaugh::_irysLaugh::_irysLaugh::_irysLaugh::_irysLaugh::_irysLaugh::_irysLaugh::_irysLaugh:
RIPRyS
hahahahaha
LMAO
F
Irys gets cocky
:_irysLaugh::_irysLaugh::_irysLaugh:OMG
IRyS...
LMAOOO
LOL
LETS GOO!
lool
:_irysLaugh::_irysLaugh::_irysLaugh:
LOL
:_irysLaugh::_irysLaugh::_irysLaugh::_irysLaugh:
:_irysLaugh::_irysLaugh::_irysLaugh:
dang irys throwing
:_irysLaugh::_irysLaugh::_irysLaugh:
EZ
:_irysPatrys::_irysPatrys::_irysPatrys:
total Throw:_irysRys:
lol"""

# split the texts into tokens
sep_sentences = nltk.sent_tokenize(text)
s_tokens = []
bi_tokens = []
tri_tokens = []
for x in sep_sentences:
    tokens = nltk.word_tokenize(x)
    tokens = [token.lower() for token in tokens if len(token) > 1]
    s_tokens.extend(tokens)
    bi_tokens.extend(list(bigrams(tokens)))
    tri_tokens.extend(list(trigrams(tokens))) 

frequence = nltk.FreqDist(bi_tokens)
for key,value in frequence.items():
    print(key,value)

print(s_tokens)