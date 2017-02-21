import freqanal
import util

lfreq = ["E","T","A","O","I","N","S","R","H","L","D","C","U","M","F","P","G","W","Y","B","V","K","X","J","Q","Z"]
abc =   ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
cdi =   ["TH", "HE", "IN", "ER", "AN", "RE", "ES", "ON", "ST", "NT", "EN", "AT", "ED", "ND", "TO", "OR", "EA", "TI", "AR", "TE", "NG", "AL", "HA", "ET", "SE", "OU"]
ctri =  ["THE", "AND", "ING", "ENT", "ION", "HER", "FOR", "THA", "NTH", "INT", "ERE", "TIO", "TER", "EST", "ERS", "ATI", "HAT", "ATE", "ALL", "ETH", "HES", "VER", "HIS", "OFT", "ITH", "FTH"]
cquad = ["TION", "NTHE", "THER", "THAT", "OFTH", "THES", "WITH", "INTH", "ATIO", "OTHE", "TTHE", "DTHE", "INGT", "SAND", "STHE", "HERE", "THEC", "MENT", "THEM", "RTHE", "THEP", "FROM", "THIS", "TING", "THEI", "NGTH"]

def encodeSubstitutionCipher(msg, key):

    # Decodes a Subsititution Cipher based on a given key
    # inputs:
    #   String cipherText
    #   List[Char] key
    # outputs:
    #   String ct

    ct = ""
    for letter in msg:
        index = ord(letter.upper()) - 65
        try:
            ct += key[index]
        except IndexError as e:
            pass

    return ct.upper()


def decodeSubstitutionCipher(cipherText, key):

    # Decodes a Subsititution Cipher based on a given key
    # inputs:
    #   String cipherText
    #   List[Char] key
    # outputs:
    #   String plainText

    pt = ""
    for letter in cipherText:
        index = ord(letter.upper()) - 65
        try:
            pt += key[index]
        except IndexError as e:
            pass

    return pt.lower()

def guessSubstitutionCipher(cipherText, fe):

    # Guesses a substitution cipher key based on letter frequency
    # inputs:
    #   String cipherText
    # outputs:
    #   List[Char] key
    
    import operator
    import numpy as np

    hue = dict()
    for l in abc:
        hue[l] = dict()
    
    cipherFreq = freqanal.findCommonMonograms(cipherText)
    xfreq = sorted(cipherFreq.items(),key=operator.itemgetter(1), reverse=True)

    #######################################
    ##                                   ##
    ## I wanted this to work so badly... ##
    ##                                   ##
    #######################################
    ##
    ##
    ##    for r in xrange(0,26):
    ##        hue[xfreq[r][0]].update({lfreq[r]: 8})
    ##
    ##    commonDigrams = sorted(util.findTopN(freqanal.findCommonNGrams(cipherText, 2), 26).items(), key = operator.itemgetter(1), reverse=True)
    ##
    ##    for i in xrange(0,26):
    ##        for j in [0,1]:
    ##            if cdi[i][j] in hue[commonDigrams[i][0][j]]:
    ##                hue[commonDigrams[i][0][j]][cdi[i][j]] += 4
    ##            else:
    ##                hue[commonDigrams[i][0][j]][cdi[i][j]] = 4
    ##    
    ##    commonTrigrams = sorted(util.findTopN(freqanal.findCommonNGrams(cipherText, 3), 26).items(), key = operator.itemgetter(1), reverse=True)
    ##
    ##    for i in xrange(0,26):
    ##        for j in [0,1,2]:
    ##            if ctri[i][j] in hue[commonTrigrams[i][0][j]]:
    ##                hue[commonTrigrams[i][0][j]][ctri[i][j]] += 5
    ##            else:
    ##                hue[commonTrigrams[i][0][j]][ctri[i][j]] = 5
    ##    
    ##    commonQgrams = sorted(util.findTopN(freqanal.findCommonNGrams(cipherText, 4), 26).items(), key = operator.itemgetter(1), reverse=True)
    ##
    ##    for i in xrange(0,26):
    ##        for j in [0,1,2,3]:
    ##            if cquad[i][j] in hue[commonQgrams[i][0][j]]:
    ##                hue[commonQgrams[i][0][j]][cquad[i][j]] += 1
    ##            else:
    ##                hue[commonQgrams[i][0][j]][cquad[i][j]] = 1
    ##
    ##    for r in hue.keys():
    ##        for x in hue[r].keys():
    ##            hue[r][x] = float(hue[r][x]) ** 2
    ##        t = sum(hue[r].values())
    ##        for x in hue[r].keys():
    ##            hue[r][x] = float(hue[r][x])/float(t)
    ##
    ##    maxs = -10000000000000000
    ##    maxk = ""
    ##    count = 0
    ##
    ##    initial_wew = ""
    ##
    ##    #for 
    ##
    ##    while count < 1:
    ##        wew = list("___X______________________")
    ##        for r in abc:
    ####            print r
    ####            print "     ", hue[r].keys()
    ####            print "     ", hue[r].values()
    ##            s1 = [m for m in hue[r].keys() if m not in list(wew)]
    ##            t = 0
    ##            for x in  s1:
    ##                t += hue[r][x]
    ##            print s1, len(s1)
    ##            s2 = [hue[r][m]/t for m in s1]
    ##            print s2, len(s2)
    ##
    ##            if len(s1) == 0 and len(s2) == 0:
    ##                s1 = [m for m in abc if m not in list(wew)]
    ##                s2 = [float(1)/float(len(s1)) for m in xrange(0,len(s1))]
    ##            
    ##            x = np.random.choice(s1, p=s2)
    ##            print x, "\n"
    ##            wew[abc.index(r)] = x[0]
    ##
    ##        de = decodeSubstitutionCipher(cipherText, wew)
    ##        ems = fe.score(cipherText)
    ##        print "     > ", wew, ems
    ##        count += 1
    ##        if ems > maxs:
    ##            maxs = ems
    ##            maxk = wew
    ##
    ##    wew = maxk

    m = []
    for l in xfreq:
        m.append(l[0])
    output = ""
    for i in abc:
        rank = m.index(i)
        output += lfreq[rank]
    return list(output)

def attackSubstitutionCipher(cipherText, fitnessEvaluator):

    # Guesses a substitution cipher key based on simulated annealing
    # inputs:
    #   String cipherText
    # outputs:
    #   List[Char] key
    
    import numpy as np
    import operator

    guess = guessSubstitutionCipher(cipherText, fitnessEvaluator)

    print "   > PT: ", abc
    print "   > CT: ", guess

    key = userInputSubCipher(cipherText, guess)
    return key


def userInputSubCipher(cipherText, guess):

    # Takes in user input to convert Cipher Text to Plain Text
    # The initial key is based on a frequency analysis guess
    # inputs:
    #   String cipherText
    #   dict(Char, Char) guess
    # outputs:
    #   String uFreq (key)
    
    key = guess
    output = ""
    output = decodeSubstitutionCipher(cipherText, key)
    print "     - CT: " + cipherText[:min(100, len(cipherText))]
    print "     - PT: " + output[:min(100, len(cipherText))]
    while True:
        toChange = raw_input('     Cipher Text Letter: ').upper()
        if toChange.lower() == 'cancel' or toChange.lower() == "quit":
            break
        changeTo = raw_input('     Plain Text Letter:  ').upper()
        if changeTo.lower() == 'cancel' or changeTo.lower() == 'quit':
            break
        key[abc.index(toChange)] = changeTo
        output = decodeSubstitutionCipher(cipherText, key)
        print "     - CT: " + cipherText[:min(100, len(cipherText))]
        print "     - PT: " + output[:min(100, len(cipherText))]
    return key

def testMethods():

    # Internal testing so I don't have to run the entire project file
    # DO NOT RUN FROM OUTSIDE THIS FILE!
    
    print " > TESTING SUBSTITUTION <\n"
    Host = util.decryptionHost(csr="../ciphertext/cipher2.txt")
    print freqanal.indexOfCoincidence(Host.cipherText)
    k = attackSubstitutionCipher(Host.cipherText)
    # decodeSubstitutionCipher(Host.cipherText, k)
