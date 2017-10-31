import sys
import getopt
from PIL import Image, ImageFilter

def usage ():
    print("usage")

def getLSB(num): #returns least significant bit of number
    mask = int('00000001', 2)
    return mask & num

#https://stackoverflow.com/questions/40557335/binary-to-string-text-in-python
def decode_binary_string(s):
    return ''.join(chr(int(s[i*8:i*8+8],2)) for i in range(len(s)//8))

def getBit(num, bitPlace): #returns the selected bit
    num = num >> bitPlace
    mask = int('00000001', 2)
    return mask & num

def placeLSB(num, bit): #places bit in LSB of num
    #print(bin(num))
    #print(bin(bit))
    mask = int('00000001', 2)
    mask = ~mask
    result = mask & num
    result = result | bit
    #print("result: " + bin(result))
    return result

#https://stackoverflow.com/questions/10237926/convert-string-to-list-of-bits-and-viceversa
def tobits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result

def frombits(bits):
    chars = []
    for b in range(len(bits) / 8):
        byte = bits[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)

def main():

    option = 0 #1-embed 2-extract
    fName = ""
    msg = ""
    outName = ""
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "m:x:", ["help"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print("Invalid Input")  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    output = None
    verbose = False
    for o, a in opts:
        if o == "-m":
            print("embedding...")
            fName = str(a)
            #print(fName)
            option = 1
            msg = input("Message to embed: ")
            outName = input("Name of new image: ")
        elif o in ("-x"):
            print("extracing...")
            fName = str(a)
            #print(fName)
            option = 2
        else:
            assert False, "unhandled option"
    #print("end of getopt")

    if option == 1:
        #variables
        #once initialized, these variables won't change
        width = 0
        height = 0
        msgLength = 0
        inputMsg = ""
        #img = Image.open(...)
        #pixel = img.load()
        msgBits = []

        #these working variables are changed often
        red = 0
        green = 0
        blue = 0
        widthIndex = 0
        heightIndex = 0
        bitIndex = 0
        charIndex = 0
        bit = 0
        char = 'a'

        #input file
        try:
            img = Image.open(fName)
        except:
            print ("Unable to load image")

        #initialize
        pixel = img.load()

        #get width & height to iterate over
        width, height = img.size
        #print("w: " + repr(width) + "  h: " + repr(height))

        #get input msg
        inputMsg = msg
        msgLength = len(inputMsg) * 8
        #print("msgLength: " + repr(msgLength))

        #embed msgLength in bottom right 11 pixels
        bitIndex = 31
        for i in range(width-1, width-12, -1):
            red, green, blue = pixel[i,height-1]
            print("r: " + repr(red) + "  g: " + repr(green) + "  b: " + repr(blue))
            print("r: " + bin(red) + "  g: " + bin(green) + "  b: " + bin(blue))
            
            bit = getBit(msgLength, bitIndex)
            bitIndex = bitIndex - 1
            red = placeLSB(red, bit)
            print("bitIndex: " + repr(bitIndex + 1))
            print("   bit: " + bin(bit))
            print("   red: " + bin(red))
            
            bit = getBit(msgLength, bitIndex)
            bitIndex = bitIndex - 1
            green = placeLSB(green, bit)
            print("bitIndex: " + repr(bitIndex + 1))
            print("   bit: " + bin(bit))
            print("   grn: " + bin(green))
            
            if i != width-11: #skip blue on 11th pixel
                bit = getBit(msgLength, bitIndex)
                bitIndex = bitIndex - 1
                blue = placeLSB(blue, bit)
                print("bitIndex: " + repr(bitIndex + 1))
                print("   bit: " + bin(bit))
                print("   blu: " + bin(blue))
            pixel[i,height-1] = red, green, blue

        msgBits = tobits(inputMsg)
        print(msgBits)
        bitIndex = 0
        print("msgBits length: " + repr(len(msgBits)))

        poo = bitIndex
        while poo >= 0:
            print(repr(poo) + ": " + repr(msgBits[poo]))
            poo = poo-1
        
        widthIndex = width-12
        heightIndex = height-1
        while bitIndex < len(msgBits):
            red, green, blue = pixel[widthIndex, heightIndex]
            wPrev = widthIndex
            hPrev = heightIndex
            print("pixel: " + repr(widthIndex) + "x" + repr(heightIndex))
            print("r: " + repr(red) + "  g: " + repr(green) + "  b: " + repr(blue))
            print("r: " + bin(red) + "  g: " + bin(green) + "  b: " + bin(blue))
            if widthIndex != 0:
                widthIndex = widthIndex - 1
            else:
                widthIndex = width - 1
                heightIndex = heightIndex - 1

            red = placeLSB(red, msgBits[bitIndex])
            print("\tbitIndex: " + repr(bitIndex))
            #print("\tbit: " + bin(msgBits[bitIndex]))
            bitIndex = bitIndex + 1
            if bitIndex >= len(msgBits):
                pixel[wPrev, hPrev] = red, green, blue
                break
            #print("\tred: " + bin(red))

            green = placeLSB(green, msgBits[bitIndex])
            print("\tbitIndex: " + repr(bitIndex))
            #print("\tbit: " + bin(msgBits[bitIndex]))
            bitIndex = bitIndex + 1
            if bitIndex >= len(msgBits):
                pixel[wPrev, hPrev] = red, green, blue
                break
            #print("\tgrn: " + bin(green))

            blue = placeLSB(blue, msgBits[bitIndex])
            print("\tbitIndex: " + repr(bitIndex))
            #print("\tbit: " + bin(msgBits[bitIndex]))
            bitIndex = bitIndex + 1
            if bitIndex >= len(msgBits):
                pixel[wPrev, hPrev] = red, green, blue
                break
            #print("\tblu: " + bin(blue))
            pixel[wPrev, hPrev] = red, green, blue
            red, green, blue = pixel[wPrev, hPrev]
            print("\tr: " + repr(red) + "  g: " + repr(green) + "  b: " + repr(blue))
            print("\tr: " + bin(red) + "  g: " + bin(green) + "  b: " + bin(blue))
            
        img.save(outName)
        print("...done")
    elif option == 2:
        #variables
        #once initialized, these variables won't change
        width = 0
        height = 0
        msgLength = 0
        outputMsg = ""
        #img = Image.open(...)
        #pixel = img.load()

        #these working variables are changed often
        red = 0
        green = 0
        blue = 0
        binaryString = ""
        widthIndex = 0
        heightIndex = 0
        bitIndex = 0

        #input file
        try:
            img = Image.open(fName)
        except:
            print ("Unable to load image")

        #initialize
        pixel = img.load()

        #get width & height to iterate over
        width, height = img.size
        #print("w: " + repr(width) + "  h: " + repr(height))

        #get length of string from bottom-right 11 pixels in image
        binaryString = ""
        for i in range(width-1, width-12, -1):
            red, green, blue = pixel[i,height-1]
            #print("r: " + repr(red) + "  g: " + repr(green) + "  b: " + repr(blue))
            #print("r: " + bin(red) + "  g: " + bin(green) + "  b: " + bin(blue))
            red   = getLSB(red)
            green = getLSB(green)
            blue  = getLSB(blue)
            #print("r: " + repr(red) + "  g: " + repr(green) + "  b: " + repr(blue))
            binaryString = binaryString + str(red) + str(green)
            if i != width-11: #skip blue on 11th pixel
                binaryString = binaryString + str(blue)
        msgLength = int(binaryString, 2)
        #print(msgLength)

        #get chars from binary in image
        binaryString = ""
        widthIndex = width-12
        heightIndex = height-1
        bitIndex = msgLength
        while bitIndex != 0:
            red, green, blue = pixel[widthIndex, heightIndex]
            if widthIndex != 0:
                widthIndex = widthIndex - 1
            else:
                widthIndex = width - 1
                heightIndex = heightIndex - 1
            red   = getLSB(red)
            green = getLSB(green)
            blue  = getLSB(blue)

            binaryString = binaryString + str(red)
            bitIndex = bitIndex - 1
            if bitIndex == 0:
                break
            binaryString = binaryString + str(green)
            bitIndex = bitIndex - 1
            if bitIndex == 0:
                break
            binaryString = binaryString + str(blue)
            bitIndex = bitIndex - 1
            if bitIndex == 0:
                break
        outputMsg = decode_binary_string(binaryString)
        print(outputMsg)
    
    print("...done")

if __name__ == "__main__":
    main()
