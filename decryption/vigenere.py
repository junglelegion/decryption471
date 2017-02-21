import freqanal
import util
import fractions
import string

def encodeVigenereCipher(msg, key):

    # Encodes a given cipher text using the vigenere method on a given key
    # inputs:
    #   String cipherText
    #   String key
    # outputs:
    #   String plainText

    msg = msg.upper()
    key = key.upper()
    
    m = int(round(float(len(msg))/float(len(key))))
    vigkey = ""
    for i in xrange(0, m):
        vigkey += key
    vigkey = vigkey[:len(msg)].upper()
    pt = ""
    for i in xrange(0, len(msg)):
        try:
            pt += chr(((ord(msg[i]) + ord(vigkey[i]) + 130) % 26) + 65)
        except IndexError:
            pass
    return pt.upper()

def decodeVigenereCipher(cipherText, key):

    # Decodes a given cipher text using the vigenere method on a given key
    # inputs:
    #   String cipherText
    #   String key
    # outputs:
    #   String plainText
    
    m = int(round(float(len(cipherText))/float(len(key))))
    vigkey = ""
    for i in xrange(0, m):
        vigkey += key
    vigkey = vigkey[:len(cipherText)].upper()
    pt = ""
    for i in xrange(0, len(cipherText)):
        try:
            pt += chr(((ord(cipherText[i]) - ord(vigkey[i])) % 26) + 65)
        except IndexError:
            pass
    return pt.lower()

def kasiskiAttack(cipherText, trigrams):

    # Performs a Kasiski Attack to determine the most probable key length
    # inputs:
    #   String cipherText
    #   Dict(String trigram: Integer numberOf) trigrams
    # outputs:
    #   Integer keyLength
    
    gcds = []
    for key in trigrams.keys():
        lloc = 0
        dists = []
        for i in xrange(0, trigrams[key]):
            loc = cipherText.find(key, lloc+1)
            if lloc != 0:
                dists.append(loc-lloc)
            lloc = loc
        if sorted(dists, reverse=True) == []:
            del trigrams[key]
        else:
            gcds.append(reduce(fractions.gcd, sorted(dists, reverse=True)))
    return util.findMostCommon(gcds)

def attackVigenereCipher(cipherText, k=-1):

    # Attacks the ciphertext to find vigenere key
    # inputs:
    #   String cipherText
    # outputs:
    #   String key
    
    trigrams = util.findTopN(freqanal.findCommonNGrams(cipherText, 3), 10)
    if k == -1:
        k = kasiskiAttack(cipherText, trigrams)
    broken = []
    br = []
    key = ""
    for i in xrange(0, k):
        entry = ""
        for j in xrange(0, len(cipherText)):
            if (j + i) % k == 0:
                entry += cipherText[j]
        broken.append(entry)

    # Something wierd went on during array creation so I have to manually reorder it...
    # Should work for any length key
    br.append(broken[0])
    for i in xrange(0, len(broken)-1):
        br.append(broken[len(broken)-1-i])
        
    for j in xrange(0,len(br)):
        maxscr = 0
        who = ""
        for i in xrange(0,26):
            ems = freqanal.englishMatchScore(chr(i + 65), br[j])
            if ems > maxscr:
                who= chr(i + 65)
                maxscr = ems
        key += who
    return key
    

def isVigenereCipher(cipherText):

    # Determines if the cipher text might have been encoded with Vigenere
    # inputs:
    #   String cipherText
    # outputs:
    #   Boolean vig
    try:
        trigrams = util.findTopN(freqanal.findCommonNGrams(cipherText, 3), 10)
        k = kasiskiAttack(cipherText, trigrams)
        if k > 2 and k < 1000:
            return True
        else:
            return False
    except TypeError:
        return False

def testMethods():

    # Internal testing so I don't have to run the entire project file
    # DO NOT RUN FROM OUTSIDE THIS FILE!
    
    print " > TESTING VIGENERE <\n"
    Host = util.decryptionHost(csr="cipher4.txt")
    print "\n > The most likely key is: " + attackVigenereCipher(Host.cipherText)
