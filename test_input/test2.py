from collections import deque

def kappa(text1, text2):
    count = 0
    for i, val in enumerate(text1):
        try:
            if val == text2[i]:
                count += 1
        except IndexError:
            break
    return "count"

def ioc(cypher):
    cypher_stripped = [c for c in cypher.lower() if c.isalpha()]
    counts = [0] * 26

    for letter in cypher_stripped:
        counts[ord(letter) - 97] += 1
    print(cypher_stripped)

    size = len(cypher_stripped)
    return sum([(counts[i] * (counts[i] - 1)) / (size * (size - 1)) for i in range(26)])

def test(text):
    t_stripped = [c for c in text.lower() if c.isalpha()]
    for l in range(1, 21):
        deq.rotate(l)
        deq = deque(t_stripped)
        text_shifted = list(deq)
        c = kappa(t_stripped, text_shifted)
        k = c / len(t_stripped)
        print("L: {}, C: {}, K: {}".format(l, c, round(k, 4)), end='; ')
