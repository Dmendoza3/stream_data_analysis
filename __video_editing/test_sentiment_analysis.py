from nltk.sentiment import SentimentIntensityAnalyzer

def sentiment_analysis(text):
    sia = SentimentIntensityAnalyzer()
    ret_val = sia.polarity_scores(text)
    return ret_val

print(sentiment_analysis("Wow, NLTK is really powerful!")["compound"])