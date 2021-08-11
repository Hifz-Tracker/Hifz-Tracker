import json
import random

def getRandomQuote():
    with open('quotes.json') as f:
        quotes = json.load(f)
        randomQuote = random.choice(quotes)
    return randomQuote
