def findCommonMonograms(cipherText):
    monograms = []
    freq = []
    for l in xrange(0,26):
        monograms.append(chr(l+65))
        freq.append(cipherText.count(chr(l+65)))
    return dict(zip(monograms, freq))

def findCommonDigrams(cipherText):
    digrams = []
    freq = []
    for l in xrange(0,26):
        for j in xrange(0,26):
            freq.append(cipherText.count(str(chr(l+65)+chr(j+65))))
            digrams.append(str(chr(l+65)+chr(j+65)))
    output = dict(zip(digrams, freq))
    for e in output.keys():
        if output[e] < 1:
            del output[e]
    return output

def findCommonTrigrams(cipherText):
    trigrams = dict()
    for i in xrange(0, len(cipherText)-2):
        tg = cipherText[i:i+3]
        if tg not in trigrams:
            trigrams[tg] = 1
        else:
            trigrams[tg] += 1
    return trigrams

def findCommonQuadgrams(cipherText):
    quadgrams = dict()
    for i in xrange(0, len(cipherText)-3):
        tg = cipherText[i:i+4]
        if tg not in quadgrams:
            quadgrams[tg] = 1
        else:
            quadgrams[tg] += 1
    return quadgrams

def findCommonNGrams(cipherText, n):
    ngrams = dict()
    for i in xrange(0, len(cipherText)-n-1):
        tg = cipherText[i:i+n]
        if tg not in ngrams:
            ngrams[tg] = 1
        else:
            ngrams[tg] += 1
    return ngrams

def indexOfCoincidence(cipherText):
    x = findCommonMonograms(cipherText)
    N = float(len(cipherText))
    c = float(len(x))
    d = float(N *(N-1))
    t = 0
    for i in xrange(0,len(x)):
        t += x[chr(i+65)] * (x[chr(i+65)] - 1)
    return float(t)/float(d)

def shiftedIOC(cipherTexts, n):
    import shift
    cipherText = shift.decodeShiftCipher(cipherTexts, n).upper()
    x = findCommonMonograms(cipherText)
    N = float(len(cipherText))
    c = float(len(x))
    d = float(N *(N-1))
    t = 0
    for i in xrange(0,len(x)):
        t += x[chr(i+65)] * (x[chr(i+65)] - 1)
    return float(t)/float(d)

def englishMatchScore(subKey, cipherMod):
    import operator
    import util
    subKey = subKey.upper()
    lfreq = ["E","T","A","O","I","N","S","R","H","L","D","C","U","M","F","P","G","W","Y","B","V","K","X","J","Q","Z"]
    fmono = findCommonMonograms(cipherMod)
    xfreq = sorted(fmono.items(),key=operator.itemgetter(1), reverse=True)
    score = 0
    mfreq = []
    for i in xrange(0,len(xfreq)):
        mfreq.append(chr(((ord(xfreq[i][0]) - ord(subKey)) % 26) + 65))
        xfreq[i] = xfreq[i][0]
        if util.closeBy(mfreq, lfreq, i, 4):
            score += 1
    return score

class quadgramFitness(object):
    def __init__(self):
        from math import log10
        self.quads = dict()
        with open("./dictionaries/trigrams.txt") as qFile:
            for line in qFile:
                key, value = line.split()
                self.quads[key] = int(value)
            self.totalQuads = float(sum(self.quads.values()))
            for key in self.quads.keys():
                self.quads[key] = log10(float(self.quads[key])/self.totalQuads)
            self.none = log10(0.01/self.totalQuads)
    def score(self, cipherText):
        from math import log10
        score = 0
        quadgrams = findCommonNGrams(cipherText, 4)
        for key in quadgrams.keys():
            score += self.probability(key)
        return score
    def probability(self, aq):
        if aq in self.quads:
            return self.quads[aq]
        else:
            return self.none
