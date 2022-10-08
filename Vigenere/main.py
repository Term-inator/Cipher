import re


def getIndex(char):
    return ord(char) - ord('A')


def shift(char, key):
    index = getIndex(char)
    new_index = (index + key) % 26
    return chr(new_index + ord('A'))


def encrypt(plaintext, key):
    res = ''
    for i in range(len(plaintext)):
        res += shift(plaintext[i], getIndex(key[i % len(key)]))
    return res


def decrypt(ciphertext, key):
    res = ''
    for i in range(len(ciphertext)):
        res += shift(ciphertext[i], -getIndex(key[i % len(key)]))
    return res


p = {
    0: 0.082,
    1: 0.015,
    2: 0.028,
    3: 0.042,
    4: 0.127,
    5: 0.022,
    6: 0.020,
    7: 0.061,
    8: 0.070,
    9: 0.001,
    10: 0.008,
    11: 0.040,
    12: 0.024,
    13: 0.067,
    14: 0.075,
    15: 0.019,
    16: 0.001,
    17: 0.060,
    18: 0.063,
    19: 0.090,
    20: 0.028,
    21: 0.010,
    22: 0.024,
    23: 0.020,
    24: 0.001,
    25: 0.001
}


def attack(ciphertext):
    n = len(ciphertext)
    I = [0 for d in range(n)]
    freq = [[0 for i in range(26)] for d in range(n)]
    for d in range(2, n):
        # 分组
        words = [ciphertext[i:(i+d)] for i in range(0, n, d)]
        for char in ciphertext:
            freq[d-1][getIndex(char)] += 1
        for i in range(len(freq[d-1])):
            freq[d-1][i] /= n

        eps = 0.005
        for i in range(26):
            I[d-1] += freq[d-1][i] / d * (freq[d-1][i] - 1) / (d - 1)
            if abs(I[d-1] - 0.0065) < eps:
                eps = abs(I[d-1] - 0.0065)
    return d


def removeOtherSymbol(text):
    reg = re.compile("[^a-zA-Z]")
    return re.sub(reg, "", text)


if __name__ == '__main__':
    text = '''As a magician , I try to create images that make people stop and think

I also try to challenge myself to do things that doctors say are not possible

As a magician ,I try to show things to people that seem impossible

And I think magic ,whether I am holding my breath or shuffling a deck of cards, is pretty simple

It's practice, it's training.

And it' s practice, it' s training and experimenting ,while pushing through the pain to be the best that I can be

And that's what magic is to me, so ,thank you. (Applause)'''
    text = removeOtherSymbol(text)
    text = text.upper()
    ciphertext = encrypt(text, 'TEST')
    print(f'ciphertext: {ciphertext}')
    key = attack(ciphertext)
    print(f'key: {key}')
    # plaintext = decrypt(ciphertext, 'TEST')
    # print(f'plaintext: {plaintext}')