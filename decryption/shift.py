import util

def encodeShiftCipher(message, key):

    # Encodes a given cipher text using the shift method on a given key
    # inputs:
    #   String message
    #   String key OR Integer key
    # outputs:
    #   String plainText

    key = key.upper()

    if type(key) is str:
        key = ord(key) - 65
    
    plainText = ""
    for l in message.upper():
        plainText += chr(((ord(l) - 65 + key) % 26) + 65)
    return plainText.upper()


def decodeShiftCipher(cipherText, key):

    # Decodes a given cipher text using the shift method on a given key
    # inputs:
    #   String cipherText
    #   String key OR Integer key
    # outputs:
    #   String plainText

    if type(key) is str:
        key = ord(key) - 65
    
    plainText = ""
    for l in cipherText:
        plainText += chr(((ord(l) - 65 - key) % 26) + 65)
    return plainText.lower()

def attackShiftCipher(cipherText):

    # Runs a frequency analysis attack on the cipher text to determine the shift key
    # inputs:
    #   String cipherText
    # outputs:
    #   Integer key
    
    import freqanal
    maxscr = 0
    who = ""
    for i in xrange(0,26):
        ems = freqanal.englishMatchScore(chr(i + 65), cipherText[:min(200, len(cipherText))])
        if ems > maxscr:
            who= chr(i + 65)
            maxscr = ems
    return ord(who.upper()) - 65
    
def testMethods():

    # Internal testing so I don't have to run the entire project file
    # DO NOT RUN FROM OUTSIDE THIS FILE!
    
    print " > TESTING SHIFT <\n"
    Host = util.decryptionHost(csr = "../ciphertext/ciphertext.txt")
    k = attackShiftCipher(Host.cipherText)
    print "\n > The most likely key is: " + chr(k + 65) + "(" + str(k) + ")"
    print decodeShiftCipher(Host.cipherText, k)

def isShiftCipher(cipherText, oldEMS):
    import freqanal
    i = attackShiftCipher(cipherText)
    newEMS = freqanal.englishMatchScore(chr(i + 65), cipherText)
    print "     >", newEMS
    if newEMS > 2*oldEMS-1:
        return True
    else:
        return False
