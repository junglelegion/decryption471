import util
import freqanal

def decodeColumnarTransposeCipher(cipherText, key):
    
    # Decodes a Columnar Transposition cipher based on a given key
    # inputs:
    #   String cipherText
    #   String key
    # outputs:
    #   String plainText

    cols = len(key)
    mat_orig = [[0 for x in range(len(cipherText)/cols)] for y in range(cols)]
    mat_tran = [[0 for x in range(cols)] for y in range(len(cipherText)/cols)]
    mat_final = []
    curr = 0
    keyl = []
    for l in key:
        keyl.append(l)
    keys = sorted(keyl)
    for i in range(len(mat_orig)):
        # iterate through columns
        for j in range(len(mat_orig[0])):
            mat_orig[i][j] = cipherText[curr]
            curr += 1
    for i in keyl:
        mat_final.append(mat_orig[keys.index(i)])
    for i in range(len(mat_final)):
       # iterate through columns
       for j in range(len(mat_final[0])):
           mat_tran[j][i] = mat_final[i][j]
    pt = ""
    for i in range(len(mat_tran)):
        # iterate through columns
        for j in range(len(mat_tran[0])):
            pt += mat_tran[i][j]
    
    return pt.lower()

def attackColumnarTransposeCipher(cipherText, fitnessEvaluator, k=-1):

    # Attacks a Columnar Transposition cipher with a bruteforce attack as you cannot perform frequency analysis on it
    # inputs:
    #   String cipherText
    #   String key
    # outputs:
    #   String plainText
    
    score = -1000000000000
    bestKey = ""
    if k == -1:
        n = 2
        lim = 8
    else:
        n = k
        lim = k+1
    while n < lim:
        q = util.colKeys(n)
        if len(cipherText) % n == 0:
            for i in xrange(0, len(q)):
                de = decodeColumnarTransposeCipher(cipherText, q[i])
                x = fitnessEvaluator.score(de)
                if x > score:
                    score = x
                    bestKey = q[i]
        n += 1
    return bestKey


def testMethods():

    # Internal testing so I don't have to run the entire project file
    # DO NOT RUN FROM OUTSIDE THIS FILE!
    
    print " > TESTING COLUMNAR <\n"
    Host = util.decryptionHost(csr="CT_cipher.txt")
    key = attackColumnarTransposeCipher(Host.cipherText)
    print decodeColumnarTransposeCipher(Host.cipherText, key)[:100]
