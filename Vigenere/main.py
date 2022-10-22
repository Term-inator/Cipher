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


def splitText(ciphertext, group_num):
    """
    将 ciphertext 分组
    :param ciphertext: 密文
    :param group_num: 组数
    :return: 分组后的列表 1 * group_num
    """
    groups = ['' for i in range(group_num)]
    for i in range(len(ciphertext)):
        for j in range(group_num):
            if i % group_num == j:
                groups[j] += ciphertext[i]
    return groups


def calFreq(string):
    """
    计算 string 各个字符的频数
    :param string:
    :return: 频数列表 1 * 26
    """
    freq = [0 for i in range(26)]
    for char in string:
        freq[getIndex(char)] += 1
    return freq


def calCI(freq, length):
    """
    计算 CI
    :param freq: 某个分组的频数列表
    :param length: 某个分组的长度
    :return: CI 列表
    """
    CI = 0
    for i in range(26):
        CI += freq[i] / length * (freq[i] - 1) / (length - 1)
    return CI


def printCIs(CIs):
    for d in range(1, len(CIs)):
        print(f'd={d}, CI: {CIs[d]}')


def attack(ciphertext, limit):
    """
    :param ciphertext:
    :param limit: 秘钥长度尝试的上限
    :return:
    """
    # 记录频数和CI
    freqs = [[[] for i in range(limit)] for i in range(limit)]  # d * d * 26
    CIs = [[] for i in range(limit)]

    # 破解秘钥长度
    for d in range(1, limit):
        groups = splitText(ciphertext, d)

        for i in range(d):
            freqs[d][i] = calFreq(groups[i])

        CI = []
        for i in range(d):
            CI.append(calCI(freqs[d][i], len(ciphertext) // d))
        CIs[d] = CI
    printCIs(CIs)

    eps = 0.005
    key_len = 0
    for d in range(1, limit):
        avg = sum(CIs[d]) / d  # 这里选择用均值看 CI 和 0.065 的接近程度
        if abs(avg - 0.065) < eps:
            key_len = d
            eps = abs(avg - 0.065)
    print(f'key length = {key_len}')

    # 得知秘钥长度后，开始破解秘钥内容
    groups = splitText(ciphertext, key_len)
    for i in range(key_len):
        length = len(groups[i])
        for j in range(26):
            freqs[key_len][i][j] /= length  # 将频数变成频率
    # print(freqs[key_len])

    result = [0 for i in range(key_len)]  # 存放秘钥结果
    for j in range(key_len):
        # 秘钥的每一位在对应的组中都和 Caesar 相同
        I = [0 for i in range(26)]
        eps = 0.005
        res = -1
        for key in range(0, 26):
            for i in range(26):
                I[key] += p[i] * freqs[key_len][j][(i + key) % 26]
            if abs(I[key] - 0.065) < eps:
                res = key
                eps = abs(I[key] - 0.065)
        # 所有的值偏差都超过 0.005 的话选最接近的那个
        if res == -1:
            res = I.index(min(I, key=lambda x: abs(x - 0.065)))
        result[j] = res

    # 把 result 数组转变成 秘钥字符串
    for i in range(key_len):
        result[i] = shift('A', int(result[i]))
    return ''.join(result)


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

    limit = 11  # 秘钥长度尝试的上限
    key = attack(ciphertext, limit)
    print(f'key: {key}')
    plaintext = decrypt(ciphertext, key)
    print(f'plaintext: {plaintext}')
