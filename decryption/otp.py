def encodeOTP(cipherText, key):
    if len(cipherText) == len(key):
        ct = bytearray(cipherText.upper())
        ky = bytearray(key.upper())
        output = ""
        for i in xrange(0, len(ct)):
            output += chr((ct[i] + ky[i] + 130) % 26 + 65)
        return output.upper()
    else:
        print "Insecure key. Unable to encrypt."
        return ""
        

def decodeOTP(cipherText, key):
    if len(cipherText) == len(key):
        ct = bytearray(cipherText.upper())
        ky = bytearray(key.upper())
        output = ""
        for i in xrange(0, len(ct)):
            output += chr((ct[i] - ky[i]) % 26 + 65)
        return output.lower()
    else:
        print "Insecure key. Unable to encrypt."
        return ""
