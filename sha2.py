import binascii

def main():
    print(hashSHA256("abc"))

def hashSHA256(s):
    K = ["01000010100010100010111110011000", "01110001001101110100010010010001", "10110101110000001111101111001111", "11101001101101011101101110100101", "00111001010101101100001001011011", "01011001111100010001000111110001", "10010010001111111000001010100100", "10101011000111000101111011010101",
         "11011000000001111010101010011000", "00010010100000110101101100000001", "00100100001100011000010110111110", "01010101000011000111110111000011", "01110010101111100101110101110100", "10000000110111101011000111111110", "10011011110111000000011010100111", "11000001100110111111000101110100",
         "11100100100110110110100111000001", "11101111101111100100011110000110", "00001111110000011001110111000110", "00100100000011001010000111001100", "00101101111010010010110001101111", "01001010011101001000010010101010", "01011100101100001010100111011100", "01110110111110011000100011011010",
         "10011000001111100101000101010010", "10101000001100011100011001101101", "10110000000000110010011111001000", "10111111010110010111111111000111", "11000110111000000000101111110011", "11010101101001111001000101000111", "00000110110010100110001101010001", "00010100001010010010100101100111",
         "00100111101101110000101010000101", "00101110000110110010000100111000", "01001101001011000110110111111100", "01010011001110000000110100010011", "01100101000010100111001101010100", "01110110011010100000101010111011", "10000001110000101100100100101110", "10010010011100100010110010000101",
         "10100010101111111110100010100001", "10101000000110100110011001001011", "11000010010010111000101101110000", "11000111011011000101000110100011", "11010001100100101110100000011001", "11010110100110010000011000100100", "11110100000011100011010110000101", "00010000011010101010000001110000",
         "00011001101001001100000100010110", "00011110001101110110110000001000", "00100111010010000111011101001100", "00110100101100001011110010110101", "00111001000111000000110010110011", "01001110110110001010101001001010", "01011011100111001100101001001111", "01101000001011100110111111110011",
         "01110100100011111000001011101110", "01111000101001010110001101101111", "10000100110010000111100000010100", "10001100110001110000001000001000", "10010000101111101111111111111010", "10100100010100000110110011101011", "10111110111110011010001111110111", "11000110011100010111100011110010"]
    mBlocks = getChunks(complementM(s), 512)
    m = {}
    for i in range(1, len(mBlocks) + 1):
        chunks = getChunks(mBlocks[i - 1], 32)
        for k in range(16):
            m[str(i) + ";" + str(k)] = chunks[k]
    H = {}
    H["0;0"] = "01101010000010011110011001100111"
    H["0;1"] = "10111011011001111010111010000101"
    H["0;2"] = "00111100011011101111001101110010"
    H["0;3"] = "10100101010011111111010100111010"
    H["0;4"] = "01010001000011100101001001111111"
    H["0;5"] = "10011011000001010110100010001100"
    H["0;6"] = "00011111100000111101100110101011"
    H["0;7"] = "01011011111000001100110100011001"
    a, b, c, d, e, f, g, h = "", "", "", "", "", "", "", ""
    T1, T2 = "", ""
    for i in range(1, len(mBlocks) + 1):
        w = []
        for t in range(64):
            if(0<=t and t<=15):
                w += [m[str(i) + ";" + str(t)]]
            else:
                tmp = addBin(addBin(addBin(sigma1(w[t - 2]), w[t - 7]), sigma0(w[t - 15])), w[t - 16])
                while(len(tmp)<32):
                    tmp = "0" + tmp
                w += [tmp]
        a = H[str(i - 1) + ";0"]
        b = H[str(i - 1) + ";1"]
        c = H[str(i - 1) + ";2"]
        d = H[str(i - 1) + ";3"]
        e = H[str(i - 1) + ";4"]
        f = H[str(i - 1) + ";5"]
        g = H[str(i - 1) + ";6"]
        h = H[str(i - 1) + ";7"]
        for t in range(64):
            T1 = addBin(addBin(addBin(addBin(h, sigmaM1(e)), Ch(e, f, g)), K[t]), w[t])
            T2 = addBin(sigmaM0(a), Maj(a, b, c))
            while(len(T1)<32):
                T1 = "0" + T1
            while(len(T2)<32):
                T2 = "0" + T2
            h = g
            g = f
            f = e
            e = addBin(d, T1)
            while(len(e)<32):
                e = "0" + e
            d = c
            c = b
            b = a
            a = addBin(T1, T2)
            while(len(a)<32):
                a = "0" + a
        H[str(i) + ";0"] = addBin(a, H[str(i - 1) + ";0"])
        H[str(i) + ";1"] = addBin(b, H[str(i - 1) + ";1"])
        H[str(i) + ";2"] = addBin(c, H[str(i - 1) + ";2"])
        H[str(i) + ";3"] = addBin(d, H[str(i - 1) + ";3"])
        H[str(i) + ";4"] = addBin(e, H[str(i - 1) + ";4"])
        H[str(i) + ";5"] = addBin(f, H[str(i - 1) + ";5"])
        H[str(i) + ";6"] = addBin(g, H[str(i - 1) + ";6"])
        H[str(i) + ";7"] = addBin(h, H[str(i - 1) + ";7"])
    return (str(hex(int(H[str(len(mBlocks)) + ";0"], 2))) + str(hex(int(H[str(len(mBlocks)) + ";1"], 2))) + str(hex(int(H[str(len(mBlocks)) + ";2"], 2))) + str(hex(int(H[str(len(mBlocks)) + ";3"], 2))) + str(hex(int(H[str(len(mBlocks)) + ";4"], 2))) + str(hex(int(H[str(len(mBlocks)) + ";5"], 2))) + str(hex(int(H[str(len(mBlocks)) + ";6"], 2))) + str(hex(int(H[str(len(mBlocks)) + ";7"], 2)))).replace("0x", "").replace("L", "")
                
def sigma1(x):
    return binXor(binXor(rotr(17, x), rotr(19, x)), shr(10, x))
    
def sigma0(x):
    return binXor(binXor(rotr(7, x), rotr(18, x)), shr(3, x))

def Ch(x, y, z):
    return binOr(binAnd(x, y), binAnd(binComplement(x), z))

def sigmaM1(x):
    return binXor(binXor(rotr(6, x), rotr(11, x)), rotr(25, x))

def sigmaM0(x):
    return binXor(binXor(rotr(2, x), rotr(13, x)), rotr(22, x))

def Maj(x, y, z):
    return binOr(binOr(binAnd(x, y), binAnd(x, z)), binAnd(y, z))

def rotl(n, x):
    d = x[:n]
    e = x[n:]
    return e + d

def rotr(n, x):
    for i in range(n):
        x = x[-1] + x
        x = x[:(len(x) - 1)]
    return x

def shr(n, x):
    for i in range(n):
        x = "0" + x
    x = x[:(len(x) - n)]
    return x

def addBin(x,y):
        maxlen = max(len(x), len(y))
        x = x.zfill(maxlen)
        y = y.zfill(maxlen)
        result = ''
        carry = 0
        for i in range(maxlen-1, -1, -1):
            r = carry
            r += 1 if x[i] == '1' else 0
            r += 1 if y[i] == '1' else 0
            result = ('1' if r % 2 == 1 else '0') + result
            carry = 0 if r < 2 else 1       
        if carry !=0 : result = '1' + result
        l = bin2dec(result.zfill(maxlen))
        l %= 2**32
        return dec2bin(l)
 
def txt2bin(text):
    bits = bin(int(binascii.hexlify(text.encode('utf-8', 'surrogatepass')), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def bin2txt(bits):
    n = int(bits, 2)
    return int2bytes(n).decode('utf-8', 'surrogatepass')

def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))
    
def dec2bin(n):
    c = n
    b = ""
    while c:
        b = "{}".format(c%2) + b
        c = c//2
    return b

def bin2dec(b):
    d, k = 0, 1
    for i in range(len(b)-1, -1, -1):
        if b[i]=="1":
            d += k
        k *= 2
    return d

def binAnd(x, y):
    a = ""
    while len(x)!=len(y):
        if(len(x)<len(y)):
            x = "0" + x
        else:
            y = "0" + y
    for k in range(0, len(x)):
        if(x[k]=="1" and y[k]=="1"):
            a += "1"
        else:
            a += "0"
    return a

def binComplement(x):
    a = ""
    for k in range(0, len(x)):
        if(x[k]=="0"):
            a += "1"
        else:
            a += "0"
    return a

def binOr(x, y):
    a = ""
    while len(x)!=len(y):
        if(len(x)<len(y)):
            x = "0" + x
        else:
            y = "0" + y
    for k in range(0, len(x)):
        if(x[k]=="0" and y[k]=="0"):
            a += "0"
        else:
            a += "1"
    return a

def binXor(x, y):
    a = ""
    while len(x)!=len(y):
        if(len(x)<len(y)):
            x = "0" + x
        else:
            y = "0" + y
    for k in range(0, len(x)):
        if(x[k]=="0" and y[k]=="0"):
            a += "0"
        elif(x[k]=="1" and y[k]=="1"):
            a += "0"
        else:
            a += "1"
    return a

def complementM(m):
    m = txt2bin(m)
    l = len(m)
    k = (448 % 512) - (l + 1)
    while k<0:
        k += 512
    m += "1"
    for _ in range(k):
        m += "0"
    d = dec2bin(l)
    while(len(d)<64):
        d = "0" + d
    m += d
    return m

def getChunks(x, n):
    return [x[i:i+n] for i in range(0, len(x), n)]
    
if __name__ == '__main__':
    main()