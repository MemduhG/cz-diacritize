from collections import Counter
from itertools import product

def tokenize(line):
    out = []
    for item in line.strip().split(" "):
        word = item
        for sign in "„…,.?!;()“":
            word = word.replace(sign,"")
        out.append(word)
    return out


def alternatives(fname="data/map.txt"):
    d, one_to_one = {}, {}
    with open(fname) as infile:
        for line in infile:
            a, b = [x.strip() for x in line.split(";")]
            one_to_one[a] = b
            try: d[b].append(a)
            except KeyError: d[b] = [a]
    return one_to_one, d


def read_data(fname="data/corpus_ebooks"):
    with open(fname) as infile:
        lines = [line.strip("\n").rstrip().replace('\xad', '') for line in infile]
    return lines


def permutations(word, alts, counts):
    print(word)
    lists = []
    for letter in word:
        if letter in alts:
            templist = alts[letter]
            templist.append(letter)
            lists.append(templist)
        else: lists.append([letter])
    candidates = []
    products = ["".join(x) for x in product(*lists)]
    best = sorted(products, key=lambda x: counts[x], reverse=True) 
    return best[0]

def diacritize(sentence, alts, counts):
    out = []
    for token in sentence:
        if token in counts:
            out.append(token)
        else:
            out.append(permutations(token, alts, counts))
    return out

def unmark(sentence, mapping):
    tokenized = tokenize(sentence)
    out = []
    for item in tokenized:
        word = item
        for letter in mapping:
            word.replace(letter, mapping[letter])
        out.append(word)
    return out

def experiment(lines):
    train, test = lines[:50000], lines[50000:]
    words = Counter()
    for line in train:
        words.update(tokenize(line))
    ones, alt = alternatives()
    total, correct = 0, 0
    for line in test:
        print(line)
        if len(line)==0: continue
        tokenized = tokenize(line)
        diacritized = diacritize(unmark(line, ones), alt, words)
        for c, _ in enumerate(tokenized):
            if tokenized[c] == diacritized[c]:
                correct +=1
            total += 1
    print(correct, total)


if __name__ == "__main__":
    data = read_data()
    experiment(data)
