import numpy as np
import re
import string
from collections import Counter

#read words not sentences 
def read_corpus(filename):
    with open(filename, "r") as file:
        lines = file.readlines()
        words = []
        
        for line in lines:
            words += re.findall(r'\w+', line.lower())
        
    return words
words = read_corpus("autocorrect/big.txt")#change this to your corpus
vocabs = set(words) #can only have unique items 
word_counts = Counter(words)
total_word_count = float(sum(word_counts.values()))#to make floating point divisions as we play wiht probs
word_probas = {word: word_counts[word] / total_word_count for word in word_counts.keys()} #for every word in word count, get it devided with total words to get probability

def split(word):
    return [(word[:i], word[i:]) for i in range(len(word) + 1)]

def delete(word):
    return [l + r[1:] for l,r in split(word) if r]

def swap(word):
    return[l + r[1] + r[0] + r[2:] for l,r in split(word) if len(r)>1]

def replace(word):
    letters = string.ascii_lowercase
    return [l + c +r[1:] for l,r in split(word) if r for c in letters]

def insert(word):
    letters = string.ascii_lowercase
    return [l + c + r for l,r in split(word) for c in letters]

def edit1(word):
    return set(delete(word) + swap(word) + replace(word) + insert(word))

def edit2(word):
    return set(e2 for e1 in level_one_edits(word) for e2 in level_one_edits(e1))

def correct_spelling(word, vocabulary, word_probabilities):
    if word in vocabulary:
        print(f"{word} is already correctly spelt")
        return 

    suggestions = edit1(word) or edit2(word) or [word]
    best_guesses = [w for w in suggestions if w in vocabulary]
    return [(w, word_probabilities[w]) for w in best_guesses]






word = "wrod" #put your word here
corrections = correct_spelling(word, vocabs, word_probas)
if corrections:
    print(corrections)
    probs = np.array([c[1] for c in corrections])
    best_ix = np.argmax(probs)
    correct = corrections[best_ix][0]
    print(f"{correct} is suggested for {word}")
    
