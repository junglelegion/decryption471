import re
import time
import sys
import signal
import string
import freqanal

class SkipException(Exception):
    pass
def signal_handler(signal, frame):
    raise SkipException
signal.signal(signal.SIGINT, signal_handler);

class timerUtility(object):
    def __init__(self):
        self.t = 0
        self.running = False
    def begin(self):
        if not self.running:
            self.t = int(round(time.time() * 1000))
            self.running = True
            return self.t
        else:
            return False
    def end(self):
        if self.running:
            x = int(round(time.time() * 1000)) - self.t
            self.running = False
            self.t = 0
            print " > Timer Finished in " + str(x) + "ms"
            return x
        else:
            return False
    def isRunning(self):
        return self.running
    def currentTime(self):
        if self.running:
            x = int(round(time.time() * 1000)) - self.t
            return x
        else:
            return False
    def wait(self, time):
        self.begin()
        while self.currentTime() < time:
            pass
        self.running = False
        self.t = 0

class decryptionHost(object):
    def __init__(self, csr="../ciphertext/cipher1.txt"):
        #self.enWords = createDictionary(wd)
        #defineGlobalDictionary(self.enWords)
        try:
            self.file = csr
            self.fitnessEvaluator = freqanal.quadgramFitness()
            with open(csr) as ct:
                self.cipherText = ct.read().upper().replace(' ', '').translate(None, string.punctuation).replace('\n', '')
                print " > Successfully opened and processed \"" + csr +"\"!"
        except IOError as e:
            print " > Failed to open \"" + csr +"\"!"

def findMostCommon(array):
    w = dict()
    for i in xrange(0, len(array)):
        if array[i] not in w:
            w[array[i]] = 1
        else:
            w[array[i]] += 1
    import operator
    top = dict(sorted(w.iteritems(), key=operator.itemgetter(1), reverse=True)[:1])
    if any(top):
        return top.keys()[0]
    else:
        return 1

def findTopN(A, n):
    import operator
    newA = dict(sorted(A.iteritems(), key=operator.itemgetter(1), reverse=True)[:n])
    return newA

def findN(A, n):
    import operator
    newA = dict(sorted(A.iteritems(), key=operator.itemgetter(1), reverse=True)[n])
    return newA

def closeBy(array1, array2, loc, within):
    len2 = len(array2) - 1
    value = array1[loc]
    if loc-within < 0:
        lower_range = 0
    else:
        lower_range = loc - within
    if loc + within > len2:
        upper_range = len2
    else:
        upper_range = loc + within
    for i in xrange(lower_range, upper_range):
        if array2[i] == value:
            return True
    return False

def colKeys(n):
    import itertools
    letters = []
    for i in xrange(0,n):
        letters.append(chr(i+65))
    pr = list(itertools.permutations(letters))
    q = []
    for i in xrange(0, len(pr)):
        q.append(''.join(pr[i]))
    return q

def determineCipherType(cipherText):
    import freqanal
    import vigenere
    import shift
    ioc = freqanal.indexOfCoincidence(cipherText)
    print " > Determining Cipher Type:"
    ems = freqanal.englishMatchScore("A", cipherText)
    print "   > English Frequency Score:", ems
    if ems > 15:
        print "     > Transposition Cipher\n       > Columnar Transpose"
        return 4
    print "   > Index of Coincidence:", ioc
    if ioc < 0.055:
        print "     > Polyalphabetic Cipher"
        if vigenere.isVigenereCipher(cipherText):
            print "       > Vignere"
            return 3
        else:
            print "       > One Time Pad"
            return 5
    else:
        print "     > Monoalphabetic Cipher"
        sioc = freqanal.shiftedIOC(cipherText, 4)
        print "     > Shifted Index of Coincidence:", sioc
        if shift.isShiftCipher(cipherText, ems):
            print "       > Shift Cipher"
            return 1
        else:
            print "       > Substitution Cipher"
            return 2

def agrampls(n):
    if n == 1:
        return "Mono"
    elif n == 2:
        return "Di"
    elif n == 3:
        return "Tri"
    elif n == 4:
        return "Quad"
    elif n == 5:
        return "Penta"
    elif n == 6:
        return "Hexa"
    else:
        return str(n) + "-"

def testMethods():

    # Internal testing so I don't have to run the entire project file
    # DO NOT RUN FROM OUTSIDE THIS FILE!
    
    print " > TESTING UTIL <\n"
    Host = decryptionHost(csr="./ciphertext/ciphertext.txt", wd="./dictionaries/words.txt")
    determineCipherType(Host.cipherText)
