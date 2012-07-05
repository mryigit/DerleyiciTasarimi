from stack import *

def etiket_uret(i):
    return "label" + str(i)
def reguret(i):
    return "R" + str(i)

def dosya_oku(dosya_adi):
    f = open(dosya_adi , "r")
    tok_list = []
    for i in f.read().split('\n'):
        tok_list.append(i)
    f.close()
    return tok_list


def carpma(liste, index, i, dosya):
    dosya.write( "load A , %s\n"%(liste[index-1]))
    dosya.write( "mul %s\n"%(liste[index+1]))
    dosya.write( "sta "+reguret(i)+"\n")
    t = reguret(i)
    del liste[index-1:index+2]
    liste.insert(index-1, t)
    return liste

def bolme(liste, index, i, dosya):
    dosya.write( "load A , %s\n"%(liste[index-1]))
    dosya.write( "div %s\n"%(liste[index+1]))
    dosya.write( "sta "+reguret(i)+"\n")
    t = reguret(i)
    del liste[index-1:index+2]
    liste.insert(index-1, t)
    return liste

def toplama(liste, index, i, dosya):
    dosya.write( "load A , %s\n"%(liste[index-1]))
    dosya.write( "add %s\n"%(liste[index+1]))
    dosya.write( "sta "+reguret(i)+"\n")
    t = reguret(i)
    del liste[index-1:index+2]
    liste.insert(index-1, t)
    return liste

def cikarma(liste, index, i, dosya):
    dosya.write( "load A , %s\n"%(liste[index-1]))
    dosya.write( "sub %s\n"%(liste[index+1]))
    dosya.write( "sta "+reguret(i)+"\n")
    t = reguret(i)
    del liste[index-1:index+2]
    liste.insert(index-1, t)
    return liste


def bukuk(kosul, symbol_table, label, stack, kosul_eleman, dosya):
    etiket = [etiket_uret(label), etiket_uret(label+1)]
    kosul_eleman[etiket[0]] = kosul
    label += 2
    stack.push(etiket[1])
    if kosul[1] == '<':

                dosya.write( "load A , %s\n"%(kosul[0]))
                dosya.write( "cmp A , %s\n"%(kosul[2]))
                dosya.write( "jb "+ etiket[0]+"\n")
                dosya.write( "jump "+ etiket[1]+"\n")
                dosya.write( "%s:\n"%(etiket[0]))

    elif kosul[1] == '>':

                dosya.write( "load A , %s\n"%(kosul[0]))
                dosya.write( "cmp A , %s\n"%(kosul[2]))
                dosya.write( "ja "+ etiket[0]+"\n")
                dosya.write( "jump "+ etiket[1]+"\n")
                dosya.write( "%s:\n"%(etiket[0]))

    elif kosul[1] == '>=':

                dosya.write( "load A , %s\n"%(kosul[0]))
                dosya.write( "cmp A , %s\n"%(kosul[2]))
                dosya.write( "jae "+ etiket[0]+"\n")
                dosya.write( "jump "+ etiket[1]+"\n")
                dosya.write( "%s:\n"%(etiket[0]))

    elif kosul[1] == '<=':

                dosya.write( "load A , %s\n"%(kosul[0]))
                dosya.write( "cmp A , %s\n"%(kosul[2]))
                dosya.write( "jbe "+ etiket[0]+"\n")
                dosya.write( "jump "+ etiket[1]+"\n")
                dosya.write( "%s:\n"%(etiket[0]))

    else:

                dosya.write( "load A , %s\n"%(kosul[0]))
                dosya.write( "cmp A , %s\n"%(kosul[2]))
                dosya.write( "je "+ etiket[0]+"\n")
                dosya.write( "jump "+ etiket[1]+"\n")
                dosya.write( "%s:\n"%(etiket[0]))

    return label, stack, kosul_eleman



def coklu_atama(liste, atancak, dosya):
    i = 1
    while True:
        if '*' in liste:
            liste = carpma(liste, liste.index('*'), i, dosya)
            i = i + 1
        elif '/' in liste:
            liste = bolme(liste, liste.index('/'), i, dosya)
            i = i + 1
        elif '+' in liste:
            liste = toplama(liste, liste.index('+'), i, dosya)
            i = i + 1
        elif '-' in liste:
            liste = cikarma(liste, liste.index('-'), i, dosya)
            i = i + 1
        else:
            break
    dosya.write( "mov %s , %s\n"%(atancak,liste[0]))



def kosul(liste, index, symbol_table, label, stack, kosul_eleman, dosya):
    
    kosul = liste[index + 1:index + liste.index('then')]
    
    label, stack, kosul_eleman = bukuk(kosul, symbol_table, label, stack, kosul_eleman, dosya)
    
    return label, stack, kosul_eleman

def elsekosul(kosul, index, symbol_table, label, stack, kosul_eleman, dosya):
  
    if kosul[1] == '<':
        kosul[1] = '>='
    else:
        kosul[1] = '<='
        
    label, stack, kosul_eleman = bukuk(kosul, symbol_table, label, stack, kosul_eleman, dosya)
    
    return label, stack, kosul_eleman

def atama(liste, index, tablo, dosya):
    list_num = liste[index:].index(';')
    mlist = liste[index + 1 : index + liste[index:].index(';')]
    atancak = liste[index-1]
    if list_num == 2:
        if liste[index+1] in tablo:
            tablo[liste[index-1]] = tablo[liste[index+1]]
            dosya.write( "mov %s , %s\n"%(liste[index-1], tablo[liste[index+1]]))
        else:
            tablo[liste[index-1]] = liste[index+1]
            dosya.write( "mov %s , %s\n"%(liste[index-1], liste[index+1]))
    else:
        coklu_atama(mlist, atancak, dosya)
    return tablo

def untiloop(tok_list, index, symbol_table, label, stack, dosya):
    mlist = tok_list[index + 1 : index + tok_list[index:].index(';')]
    if mlist[1] == '<':
        if mlist[0] in symbol_table:
            if mlist[2] in symbol_table:
                dosya.write( "load A , %s\n"%(symbol_table[mlist[0]]))
                dosya.write( "cmp A , %s\n"%(symbol_table[mlist[2]]))
                dosya.write( "jae "+ stack.pop()+"\n")
                
            else:
                dosya.write( "load A , %s\n"%(symbol_table[mlist[0]]))
                dosya.write( "cmp A , %s\n"%(mlist[2]))
                dosya.write( "jae "+ stack.pop()+"\n")
                
        else:
            if mlist[2] in symbol_table:
                dosya.write( "load A , %s\n"%(mlist[0]))
                dosya.write( "cmp A , %s\n"%(symbol_table[mlist[2]]))
                dosya.write( "jae "+ stack.pop()+"\n")
                
            else:
                dosya.write( "load A , %s\n"%(mlist[0]))
                dosya.write( "cmp A , %s\n"%(mlist[2]))
                dosya.write( "jae "+ stack.pop()+"\n")

    elif mlist[1] == '>=':
        if mlist[0] in symbol_table:
            if mlist[2] in symbol_table:
                dosya.write ("load A , %s\n"%(symbol_table[mlist[0]]))
                dosya.write ("cmp A , %s\n"%(symbol_table[mlist[2]]))
                dosya.write ("ja "+ stack.pop()+"\n")
                
            else:
                dosya.write ("load A , %s\n"%(symbol_table[mlist[0]]))
                dosya.write ("cmp A , %s\n"%(mlist[2]))
                dosya.write ("ja "+ stack.pop()+"\n")
                
        else:
            if mlist[2] in symbol_table:
                dosya.write( "load A , %s\n"%(mlist[0]))
                dosya.write( "cmp A , %s\n"%(symbol_table[mlist[2]]))
                dosya.write( "ja "+ stack.pop()+"\n")
                
            else:
                dosya.write( "load A , %s\n"%(mlist[0]))
                dosya.write( "cmp A , %s\n"%(mlist[2]))
                dosya.write( "ja "+ stack.pop()+"\n")

    elif mlist[1] == '<=':
        if mlist[0] in symbol_table:
            if mlist[2] in symbol_table:
                dosya.write ("load A , %s\n"%(symbol_table[mlist[0]]))
                dosya.write ("cmp A , %s\n"%(symbol_table[mlist[2]]))
                dosya.write( "jb "+ stack.pop()+"\n")
                
            else:
                dosya.write ("load A , %s\n"%(symbol_table[mlist[0]]))
                dosya.write ("cmp A , %s\n"%(kosul[2]))
                dosya.write ("jb "+ stack.pop()+"\n")
                
        else:
            if mlist[2] in symbol_table:
                dosya.write( "load A , %s\n"%(mlist[0]))
                dosya.write( "cmp A , %s\n"%(symbol_table[mlist[2]]))
                dosya.write( "jb "+ stack.pop()+"\n")
            else:
                dosya.write( "load A , %s\n"%(mlist[0]))
                dosya.write( "cmp A , %s\n"%(mlist[2]))
                dosya.write( "jb "+ stack.pop()+"\n")

    elif mlist[1] == '>':
        if mlist[0] in symbol_table:
            if mlist[2] in symbol_table:
                dosya.write ("load A , %s\n"%(symbol_table[mlist[0]]))
                dosya.write ("cmp A , %s\n"%(symbol_table[mlist[2]]))
                dosya.write ("jbe "+ stack.pop()+"\n")
                
            else:
                dosya.write ("load A , %s\n"%(symbol_table[mlist[0]]))
                dosya.write ("cmp A , %s\n"%(mlist[2]))
                dosya.write ("jbe "+ stack.pop()+"\n")
        else:
            if kosul[2] in symbol_table:
                dosya.write ("load A , %s\n"%(mlist[0]))
                dosya.write ("cmp A , %s\n"%(symbol_table[mlist[2]]))
                dosya.write ("jbe "+ stack.pop()+"\n")
            else:
                dosya.write ("load A , %s\n"%(mlist[0]))
                dosya.write ("cmp A , %s\n"%(mlist[2]))
                dosya.write ("jbe "+ stack.pop()+"\n")

    else:
        dosya.write ("load A , %s\n"%(mlist[0]))
        dosya.write ("sub %s\n"%(mlist[2]))
        dosya.write ("jnz %s\n"%(stack.pop()))
                
    return stack

                
    
def labparser(label):
    return "label"+ str(label)

def arakod(yol,dosya_adi):
    stack = Stack()
    index = 0
    label = 1
    symbol_table = {}
    kosul_eleman = {}
    tok_list = dosya_oku(yol)
    dosya = open(dosya_adi, "w")
    for i in tok_list:
        if i == ':=':
            symbol_table = atama(tok_list, index, symbol_table, dosya)
            
        elif i == 'if':
            label, stack, kosul_eleman = kosul(tok_list, index, symbol_table, label, stack, kosul_eleman, dosya)
            
        elif i == 'end':
            dosya.write( "%s: nop\n"%(stack.pop()))
        elif i == 'else':
            kos = kosul_eleman[labparser(label-2)]
            label, stack, kosul_eleman = elsekosul(kos, index, symbol_table, label, stack, kosul_eleman, dosya)
        elif i == 'repeat':
            l = etiket_uret(label)
            stack.push(l)
            label = label + 1
            dosya.write( "%s:\n"%(l))
            
        elif i == 'until':
            stack = untiloop(tok_list, index, symbol_table, label, stack, dosya)

        elif i == 'write':
            dosya.write("write %s\n"%(tok_list[index + 1]))
        
        index = index + 1
    dosya.write( "hlt")
    dosya.close()



