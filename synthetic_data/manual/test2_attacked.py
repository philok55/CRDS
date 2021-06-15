from collections import deque

def kappa(text1, text3):
    count = 0
    for i, val in enumerate(text1):
        try:
            if val == text3[i]:
                count += 1
        except IndexError:
            break
    return count

def test(text):
    t_stripped = [c for c in text.lower() if c.isalpha()]
    for l in range(1, 21):
        deq = deque(t_stripped)
        deq.rotate(l)
        text_shifted = list(deq)


        c = kappa(
            text_shifted,
            t_stripped
        )
        k = c / len(t_stripped)
        print("L: {}, C: {}, K: {}".format(l, c, round(k, 4)), end='; ')

def ioc(cypher):
    counts = [0] * 26
    cypher_stripped = [c for c in cypher.lower() if c.isalpha()]

    print(cypher_stripped)
    for letter in cypher_stripped:
        counts[ord(letter) - 97] += 1

    size = len(cypher_stripped)
    return sum([(counts[i] * (counts[i] - 1)) / (size * (size - 1)) for i in range(26)])

