from decryption import *
import sys
import operator

Host = util.decryptionHost(csr=".\ciphertext\cipher4.txt")

print """  ___  ___ ___ _____   _____ _____ ___ ___  _  _   _ _ ____ _ 
 |   \| __/ __| _ \ \ / / _ \_   _|_ _/ _ \| \| | | | |__  / |
 | |) | _| (__|   /\ V /|  _/ | |  | | (_) | .` | |_  _|/ /| |
 |___/|___\___|_|_\ |_| |_|   |_| |___\___/|_|\_|   |_|/_/ |_|
 """

print " Python Version: " + sys.version
print """
 Nathaniel Christianson
 University of Arizona
 ECE 471

 Type q, quit, or press CTRL-C at any time to quit!

 Options:
   1) Please Automatically decrypt the file
   2) I know the type of cipher or key
   3) I would like to run frequency analysis on the cipher text
   4) I would like to change the file to be decrypted
   5) Please print current settings
   6) Print the options again
   7) I would like to encode a message"""

while True:
    try:
        choice = str(raw_input("\n$ "))
        if choice.isdigit():
            choice = int(choice)
        elif choice.lower() == "q" or choice.lower() =="quit":
            print " > Exiting"
            sys.exit(0)
        else:
            choice = 0
    except SkipException as e:
            print " > Exiting"
            sys.exit(0)
    if choice == 1:
        try:
            typeOfCipher = determineCipherType(Host.cipherText)
            print " > Decrypting " + Host.file + ":"
            if typeOfCipher == 1:
                print "   > Shift Cipher Decryption"
                key = shift.attackShiftCipher(Host.cipherText)
                print "   > Key: ", key, "(" + chr(key+65)+")"
                de = shift.decodeShiftCipher(Host.cipherText, key)
                print "   > Plain Text: ", de[:min(100, len(de))]
            elif typeOfCipher == 2:
                print "   > Substitution Cipher Decryption\n   > This may take a few seconds. Stand by.\n\n   *** TYPE 'QUIT' OR 'CANCEL' TO EXIT AND HAVE THE OUTPUT WRITTEN TO THE FILE! ***\n "
                key = substitution.attackSubstitutionCipher(Host.cipherText, Host.fitnessEvaluator)
                print key
                de = substitution.decodeSubstitutionCipher(Host.cipherText, key)
                print de[:min(100, len(de))]
            elif typeOfCipher == 3:
                print "   > Vigenere Cipher Decryption"
                key = vigenere.attackVigenereCipher(Host.cipherText)
                print "   > Key: ", key
                de = vigenere.decodeVigenereCipher(Host.cipherText, key)
                print "   > Plain Text: ", de[:min(100, len(de))]
            elif typeOfCipher == 4:
                print "   > Columnar Transpose Cipher Decryption"
                key = columnar.attackColumnarTransposeCipher(Host.cipherText, Host.fitnessEvaluator)
                print "   > Key: ", key
                de = columnar.decodeColumnarTransposeCipher(Host.cipherText, key)
                print "   > Plain Text: ", de[:min(100, len(de))]
            elif typeOfCipher == 5:
                print "   > One time pad is impossible to attack. Sorry.\n\n    *** If you know the key, please use option 2 and select One Time Pad from the types of ciphers listed!\n"
                de = ""
            try:
                with open("output.txt", "w+") as output:
                    output.write(de)
                    output.close()
                    print "   > Full decryption output written to output.txt"
            except IOError:
                print " > Error writing to file!"
        except SkipException as e:
            print " > Cancelled Decryption!"
    elif choice == 2:
        try:
            print """  Cipher Type:
         1) Shift Cipher
         2) Substitution Cipher
         3) Vigenere Cipher
         4) Columnar Transpose Cipher
         5) One Time Pad Cipher"""
            try:
                choice2 = str(raw_input("  $ "))
                if choice2.isdigit():
                    choice2 = int(choice2[0])
                elif choice2.lower() == "q" or choice2.lower() =="quit":
                    print " > Cancelled"
                    continue
                else:
                    choice2 = 0
                    print " > Invalid Entry"
                    continue
            except SkipException as e:
                print " > Cancelled. "
                continue
            print """  Key Information:
         1) I know the key
         2) I know the key length
         3) I don't know the key"""
            try:
                choice1 = str(raw_input("  $ "))
                if choice1.isdigit():
                    choice1 = int(choice1[0])
                elif choice1.lower() == "q" or choice1.lower() =="quit":
                    print " > Cancelled"
                    continue
                else:
                    choice1 = 0
                    print " > Invalid Entry"
                    continue
            except SkipException as e:
                print " > Cancelled. "
                continue
            if choice1 == 1:
                try:
                    keyx = str(raw_input("  $ Key (As Characters)? "))
                except SkipException as e:
                    print " > Cancelled. "
                    continue
            elif choice1 == 2 and choice2 != 1 and choice2 != 2 and choice2 != 5:
                keyx = -1
                try:
                    kl = str(raw_input("  $ Key Length? "))
                    if kl.isdigit():
                        kl = int(kl)
                    elif kl.lower() == "q" or kl.lower() =="quit":
                        print " > Cancelled"
                        continue
                    else:
                        kl = 0
                        print " > Invalid Entry"
                        continue
                except SkipException as e:
                    print " > Cancelled. "
                    continue
            else:
                keyx = -1
                kl = -1

            if choice2 == 1:
                keyx = ord(str(keyx)[0]) - 65
                print "   > Shift Cipher Decryption"
                if keyx == -20:
                    keyx = shift.attackShiftCipher(Host.cipherText)
                print "   > Key: ", keyx, "(" + chr(keyx + 65) +")"
                de = shift.decodeShiftCipher(Host.cipherText, keyx)
                print "   > Plain Text: ", de[:min(100, len(de))]
            elif choice2 == 2:
                if keyx == -1:
                    keyx = substitution.attackSubstitutionCipher(Host.cipherText, Host.fitnessEvaluator)
                else:
                    if len(keyx) != 26:
                        print "   > Invalid Key Length! Needs to be 26 characters..."
                        continue
                    print "   > Substitution Cipher Decryption\n   > This may take a few seconds. Stand by."
                print "   > Key: ", keyx
                de = substitution.decodeSubstitutionCipher(Host.cipherText, keyx)
                print "   > Plain Text: ", de[:min(100, len(de))]
            elif choice2 == 3:
                print "   > Vigenere Cipher Decryption"
                if keyx == -1:
                    if kl == -1:
                        keyx = vigenere.attackVigenereCipher(Host.cipherText)
                    else:
                        keyx = vigenere.attackVigenereCipher(Host.cipherText, k=int(kl))
                print "   > Key: ", keyx
                de = vigenere.decodeVigenereCipher(Host.cipherText, keyx)
                print "   > Plain Text: ", de[:min(100, len(de))]
            elif choice2 == 4:
                print "   > Columnar Transpose Cipher Decryption"
                if keyx == -1:
                    if kl == -1:
                        keyx = columnar.attackColumnarTransposeCipher(Host.cipherText, Host.fitnessEvaluator)
                    elif len(Host.cipherText) % kl == 0:
                        keyx = columnar.attackColumnarTransposeCipher(Host.cipherText, Host.fitnessEvaluator, k=int(kl))
                    else:
                        print "   > Invalid Key length!"
                        continue
                print "   > Key: ", keyx
                de = columnar.decodeColumnarTransposeCipher(Host.cipherText, keyx)
                print "   > Plain Text: ", de[:min(100, len(de))]
            elif choice2 == 5:
                if keyx == -1:
                    print "   > One time pad is impossible to attack. Sorry."
                    de = ""
                else:
                    if len(keyx) == len(Host.cipherText):
                        print "   > Key:", keyx[:min(100, len(keyx))]
                        de = "" + decodeOTP(Host.cipherText, keyx)
                        print "   > Plain Text:", de[:min(100, len(de))]
                    else:
                        de = ""
                        print "   > Invalid Key. len(key) != len(cipherText)"
            try:
                with open("output.txt", "w+") as output:
                    output.write(de)
                    output.close()
                    print "   > Full decryption output written to output.txt"
            except IOError:
                print " > Error writing to file!"
        except SkipException:
            print " > Cancelled."
            continue

    elif choice == 3:
        print " > Statistical Analysis"
        print " > Index of Coincidence:", freqanal.indexOfCoincidence(Host.cipherText)
        try:
            num = raw_input(" $ Up to N Grams (digram: 2, trigram: 3, etc)? ")
            if num.isdigit():
                num = int(num)
                if num < 2 or num > 10:
                    print " > You entered an invalid number!"
                    continue
            else:
                print " > You entered an invalid number!"
                continue
            amt = raw_input(" $ How many (10, 20, etc)? ")
            if amt.isdigit():
                amt = int(amt)
                if amt < 2:
                    print " > You entered an invalid number!"
                    continue
            else:
                print " > You entered an invalid number!"
                continue
            c = 1
            while c <= num:
                freq = freqanal.findCommonNGrams(Host.cipherText, c)
                output = sorted(util.findTopN(freq, min(amt, len(freq))).items(), key=operator.itemgetter(1), reverse=True)
                print " > " + util.agrampls(c) + "grams:"
                for i in output:
                    print "     ", i[0], i[1]
                c += 1
        except SkipException as e:
            print " > Cancelled!"

    elif choice == 4:
        try:
            print " > Please make sure that the file is placed in the /ciphertext/ directory!"
            filename = str(raw_input(" $ What is the file name? (with .txt) "))
            del Host
            Host = util.decryptionHost(csr="./ciphertext/" + filename)
        except SkipException as e:
            if Host:
                print " > Cancelled. Currently loaded file is: " + Host.file
            else:
                print " > Cancelled. No file loaded!"
    elif choice == 5:
        if Host:
            print " > Currently loaded file is: " + Host.file
        else:
            print " > No file loaded!"
    elif choice == 6:
        print """ Options:
   1) Please Automatically decrypt the file
   2) I know the type of cipher or key
   3) I would like to run frequency analysis on the cipher text
   4) I would like to change the file to be decrypted
   5) Please print current settings
   6) Print the options again
   7) I would like to encode a message"""
    elif choice == 7:
        try:
            print """  Cipher Type:
         1) Shift Cipher
         2) Substitution Cipher
         3) Vigenere Cipher
         4) Columnar Transpose Cipher
         5) One Time Pad Cipher"""
            try:
                choice2 = str(raw_input("  $ "))
                if choice2.isdigit():
                    choice2 = int(choice2[0])
                elif choice2.lower() == "q" or choice2.lower() =="quit":
                    print " > Cancelled"
                    continue
                else:
                    choice2 = 0
                    print " > Invalid Entry"
                    continue
            except SkipException as e:
                print " > Cancelled. "
                continue
            msg = str(raw_input("  $ Message? ")).upper().replace(' ', '').translate(None, string.punctuation).replace('\n', '')
            key = str(raw_input("  $ Key?     "))
            if choice2 == 1:
                en = shift.encodeShiftCipher(msg, key[0])
                print "  $ Encryption:", en
            elif choice2 == 2:
                en = substitution.encodeSubstitutionCipher(msg, key)
                print "  $ Encryption:", en
            elif choice2 == 3:
                en = vigenere.encodeVigenereCipher(msg, key)
                print "  $ Encryption:", en
            elif choice2 == 4:
                en = ""
                print "  > Unavailable at this time."
                print "  $ Encryption:", en
            elif choice2 == 5:
                if len(key) == len(msg):
                    en = otp.encodeOTP(msg, key)
                else:
                    print("  > Invalid Key Length!")
                    en = ""
                print "  $ Encryption:", en
            try:
                with open("./ciphertext/output.txt", "w+") as output:
                    output.write(en)
                    output.close()
                    print "   > Full encryption output written to ./ciphertext/output.txt"
            except IOError:
                print " > Error writing to file!"
        except SkipException as e:
                print " > Cancelled. "
                continue
    else:
        print " > Invalid Entry"
    
