from arakoduretec import *
from assemble import *
from hexcode import *
from hextobinary import *

def main(isim):
    yol = "C:/Users/can/Desktop/test/"
    islenecek = yol + isim + ".txt"
    kayit_ara = yol + isim + "_ara" + ".txt"
    kayit_assembly = yol + isim + "_assembly" + ".txt"
    kayit_hex = yol + isim + "_hex" + ".txt"
    kayit_binary = yol + isim + "_binary" + ".txt"
    arakod(islenecek, kayit_ara)
    assembly(kayit_ara, kayit_assembly)
    hexcode(kayit_assembly, kayit_hex)
    hextobinary(kayit_hex, kayit_binary)
