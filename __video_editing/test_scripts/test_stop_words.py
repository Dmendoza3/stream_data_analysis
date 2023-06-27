from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
  
example_sent = """LMAOOOO
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
  
stop_words = set(stopwords.words('english'))
  
reg_tokenizer = RegexpTokenizer(r"[a-zA-Z0-9]+")
word_tokens = reg_tokenizer.tokenize(example_sent)

# converts the words in word_tokens to lower case and then checks whether 
#they are present in stop_words or not
filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]

#with no lower case conversion
#filtered_sentence = [w for w in word_tokens if not w in stop_words]
  
print(word_tokens)
print(filtered_sentence)