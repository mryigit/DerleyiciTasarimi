def dosya_oku(dosya_adi):
    f = open(dosya_adi , "r")
    tok_list = []
    for i in f.read().split('\n'):
        tok_list.append(i.split(" "))
    f.close()
    return tok_list

def dectohex(sayi,ters):
    hexlist = "0123456789ABCDEF"
    liste = []
    sonuc1 =""
    while sayi !=0 :
        deger = hexlist[sayi%16]
        liste.append(deger)
        sayi = sayi/16
        
    liste.reverse()
    if ters:
        i=len(liste)
        while len(liste)<4:
            liste.insert(0,'0')
        a = liste[0] + liste[1]
        b = liste[2] + liste[3]
        sonuc = b + ' ' + a
        return sonuc
    else:
        for i in liste:
            if len(liste) < 2:
                sonuc1 ='0' + sonuc1 + i
            else:
                sonuc1 = sonuc1 + i
        return sonuc1

def hextersle(x):
    while len(x) !=5:
        x = '0' + x
    a = x[0] + x[1]
    b = x[2] + x[3]
    return b + ' ' + a

def movax(i,dosya):
    if i[3] == '[bp]':
        dosya.write( "8B 46 00\n")
    elif i[3] == 'bx':
        dosya.write( "8B C3\n")
    elif i[3][0] == '[' and i[3][len(i[3])-2] == 'h':
        dosya.write( "A1 "+dectohex(int((i[3][1:len(i[3])-2])),True) + "\n")
    else:
        dosya.write( "B8 "+dectohex(int(i[3]), True)+ "\n")

def movbx(i,dosya):
    if i[3] == '[bp]':
        dosya.write( "8B 5E 00\n")
    else:
        dosya.write( "BB "+dectohex(int(i[3]), True)+ "\n")

def movbp(i,dosya):
    if i[1] == 'bp':
        dosya.write( "BD " + hextersle(i[3])+ "\n")
    if i[1] == '[bp]':
        if i[3] == 'ax':
            dosya.write( "89 46 00\n")
        else:
            if int(i[3]) < 256:
                dosya.write( "C6 46 00 " +  dectohex(int(i[3]), True)[0:2]+ "\n")
            else:
                dosya.write( "C6 46 00 " +  dectohex(int(i[3]), True)+ "\n")
        

def ayir(k):
    conlist = []
    for i in k:
        if i[0][0:len(i[0])-2] == 'label':
            conlist.append(i)
        else:
            gecici = i[0]
            del i[0]
            i.insert(0,gecici[1:len(gecici)])
            conlist.append(i)
    return conlist

def ayir2(k):
    conlist = []
    for i in k:
        conlist.append(i)
    return conlist

def hexcode(yol,dosya_adi):
    k = dosya_oku(yol)
    dosya = open(dosya_adi , "w")
    liste = ayir(k)
    for i in liste:
        if i[0] == 'mov':
            if i[1] == 'ax':
                movax(i,dosya)
            elif i[1] == 'bx':
                movbx(i,dosya)
            elif i[1] == 'bp' or i[1] == '[bp]':
                movbp(i,dosya)
        
        elif i[0] == 'call':
            dosya.write("""E8 05 00
B4 01
CD 21
C3
3D 00 00
75 09
50
B0 30
B4 0E
CD 10
58
C3
60
BA 00 00
3D 00 00
74 12
BB 0A 00
F7 F3
E8 EF FF
8B C2
04 30
B4 0E
CD 10
EB 00
61
C3""")
            dosya.close()
            break
        elif i[0] == 'mul':
            dosya.write( "F7 E3\n")
        elif i[0] == 'div':
            dosya.write( "F7 F3\n")
        elif i[0] == 'add':
            dosya.write( "03 C3\n")
        elif i[0] == 'sub':
            dosya.write( "2B C3\n")
        elif i[0] == 'cmp':
            if i[3][0] == '[':
                dosya.write( "3B 06 " + hextersle(i[3][1:len(i[3])-1])+ "\n")
            else:
                dosya.write( "3D " + dectohex(int(i[3]), True)+ "\n")
        elif i[0] == 'ret':
            dosya.write( "C3")
        elif i[0][0:len(i[0])-2] == 'label':
            if len(i) > 1:
                if i[1] == 'nop':
                    dosya.write( i[0] + ' ' + "90\n")
            else:
                dosya.write( i[0]+ "\n")
                
        elif i[0] == 'jb':
            dosya.write( "72 " + i[1] + "\n")
        elif i[0] == 'jbe':
            dosya.write( "76 " + i[1] + "\n")
        elif i[0] == 'ja':
            dosya.write( "77 " + i[1] + "\n")
        elif i[0] == 'jae':
            dosya.write( "73 " + i[1] + "\n")
        elif i[0] == 'je':
            dosya.write( "74 " + i[1] + "\n")
        elif i[0] == 'jmp':
            dosya.write( "EB " + i[1] + "\n")
        elif i[0] == 'jnz':
            dosya.write( "75 " + i[1] + "\n")

    dosya.close()

    l = dosya_oku(dosya_adi)
    gecici = ayir2(l)
    sondizi = []
    label = {}
    index = 0
    
    for i in gecici:
        for t in range(len(i)):
            sondizi.append(i[t])
    for i in sondizi:
        if i[0:len(i)-1] == 'label':
            
            j = sondizi.index(i+':')
            if index <= j:
                tmp = sondizi[index+1:j]
                label[i] = dectohex(len(aracikar(tmp)),False)
            else:
                tmp = sondizi[j+1:index]
                label[i] = dectohex(255-len(aracikar(tmp)),False)
        index = index + 1
    dosya1 = open(dosya_adi , "w")
    index = 0
    for i in gecici:
        tlen = 0
        for t in i:
            if not ':' in t:
                durum = True
                if t[0:len(t)-1] == 'label':
                    dosya1.write(label[t])
                    if len(i)-1 != tlen:
                        dosya1.write(' ')
                    
                else:
                    dosya1.write(t)
                    if len(i)-1 != tlen:
                        dosya1.write(' ')
            
                    
            else:
                durum = False
            tlen += 1
        
        if durum and len(gecici)-1 != index:
            dosya1.write('\n')
        index += 1
    dosya1.close()

def aracikar(tmp):
    index = 0
    for i in tmp:
        if ':' in i:
            del tmp[index]
        index += 1
    return tmp
        
            
                
                
                
            
            
    
