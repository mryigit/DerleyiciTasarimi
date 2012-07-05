from stack import *

def dosya_oku(dosya_adi):
    f = open(dosya_adi , "r")
    tok_list = []
    for i in f.read().split('\n'):
        tok_list.append(i.split(" "))
    f.close()
    return tok_list

def ayir(k):
    
    tok_list = []
    for i in k:
        for t in i:
            tok_list.append(t)

    return tok_list

def loadla(tok_list, index, rstack, symbol_table, dosya):
    
    if tok_list[index+3] in symbol_table:
        x = symbol_table[tok_list[index+3]]
        dosya.write( "\tmov bp , %s\n"%(x))
        dosya.write( "\tmov ax , [bp]\n")
    elif tok_list[index+3] in rstack:
        x = symbol_table[rstack[tok_list[index+3]]]
        dosya.write( "\tmov bp , %s\n"%(x))
        dosya.write( "\tmov ax , [bp]\n")
    else:
        dosya.write( "\tmov ax , %s\n"%(tok_list[index+3]))


def mulla(tok_list, rstack, index, symbol_table, dosya):
    if tok_list[index+1] in symbol_table:
        dosya.write( "\tmov bp , %s\n"%(symbol_table[tok_list[index+1]]))
        dosya.write( "\tmov bx , [bp]\n")
        dosya.write( "\tmul bx\n")
    elif tok_list[index+1] in rstack:
        dosya.write( "\tmov bp , %s\n"%(symbol_table[rstack[tok_list[index+1]]]))
        dosya.write( "\tmov bx , [bp]\n")
        dosya.write( "\tmul bx\n")
    else:
        dosya.write( "\tmov bx , %s\n"%(tok_list[index+1]))
        dosya.write( "\tmul bx\n")

def stala(tok_list, index, rstack, symbol_table, adres, dosya):
    
    tmp = tok_list[:index]
    tmp.reverse()
    x = tmp[tmp.index('load')-3]
    if x[0] == 'R':
        rstack[tok_list[index+1]] = rstack[x]
        
        if not rstack[x] in symbol_table:
            symbol_table[rstack[x]] = str(adres)+'h'
            adres += 2
        dosya.write( "\tmov bp , %s\n"%(symbol_table[rstack[x]]))
        dosya.write( "\tmov [bp] , ax\n")
    else:
        rstack[tok_list[index+1]] = x
        
        if not x in symbol_table:
            symbol_table[x] = str(adres)+'h'
            adres += 2
        dosya.write( "\tmov bp , %s\n"%(symbol_table[x]))
        dosya.write( "\tmov [bp] , ax\n")
    
    
    
    return rstack, symbol_table, adres

def movla(tok_list, index, rstack, symbol_table, adres, dosya):
    if tok_list[index+3] in symbol_table:
        y = symbol_table[tok_list[index+3]]
        
        if not tok_list[index+1] in symbol_table:
            symbol_table[tok_list[index+1]] = str(adres)+'h'
            adres += 2
        dosya.write( "\tmov bp , %s\n"%(y))
        dosya.write( "\tmov ax , [bp]\n")
        dosya.write( "\tmov bp , %s\n"%(symbol_table[tok_list[index+1]]))
        dosya.write( "\tmov [bp] , ax\n")
        
            
    elif tok_list[index+3] in rstack:
        y = symbol_table[rstack[tok_list[index+3]]]
        if not tok_list[index+1] in symbol_table:
            symbol_table[tok_list[index+1]] = str(adres)+'h'
            adres += 2
        dosya.write( "\tmov bp , %s\n"%(y))
        dosya.write( "\tmov ax , [bp]\n")
        dosya.write( "\tmov bp , %s\n"%(symbol_table[tok_list[index+1]]))
        dosya.write( "\tmov [bp] , ax\n")
        
    else:
        if not tok_list[index+1] in symbol_table:
            symbol_table[tok_list[index+1]] = str(adres)+'h'
            dosya.write( "\tmov bp , %dh\n"%(adres))
            dosya.write( "\tmov [bp] , %s\n"%(tok_list[index+3]))
            adres += 2
        else:
            dosya.write( "\tmov bp , %s\n"%(symbol_table[tok_list[index+1]]))
            dosya.write( "\tmov [bp] , %s\n"%(tok_list[index+3]))
        
    return adres

def addle(tok_list, rstack, index, symbol_table, dosya):
    if tok_list[index+1] in symbol_table:
        dosya.write( "\tmov bp , %s\n"%(symbol_table[tok_list[index+1]]))
        dosya.write( "\tmov bx , [bp]\n")
        dosya.write( "\tadd ax , bx\n")
    elif tok_list[index+1] in rstack:
        dosya.write( "\tmov bp , %s\n"%(symbol_table[rstack[tok_list[index+1]]]))
        dosya.write( "\tmov bx , [bp]\n")
        dosya.write( "\tadd ax , bx\n")
    else:
        dosya.write( "\tmov bx , %s\n"%(tok_list[index+1]))
        dosya.write( "\tadd ax , bx\n")

def divle(tok_list, rstack, index, symbol_table, dosya):
    if tok_list[index+1] in symbol_table:
        dosya.write( "\tmov bp , %s\n"%(symbol_table[tok_list[index+1]]))
        dosya.write( "\tmov bx , [bp]\n")
        dosya.write( "\tdiv bx\n")
    elif tok_list[index+1] in rstack:
        dosya.write( "\tmov bp , %s\n"%(symbol_table[rstack[tok_list[index+1]]]))
        dosya.write( "\tmov bx , [bp]\n")
        dosya.write( "\tdiv bx\n")
    else:
        dosya.write( "\tmov bx , %s\n"%(tok_list[index+1]))
        dosya.write( "\tdiv bx\n")

def subla(tok_list, rstack, index, symbol_table, dosya):
    if tok_list[index+1] in symbol_table:
        dosya.write( "\tmov bp , %s\n"%(symbol_table[tok_list[index+1]]))
        dosya.write( "\tmov bx , [bp]\n")
        dosya.write( "\tsub ax , bx\n")
    elif tok_list[index+1] in rstack:
        dosya.write( "\tmov bp , %s\n"%(symbol_table[rstack[tok_list[index+1]]]))
        dosya.write( "\tmov bx , [bp]\n")
        dosya.write( "\tsub ax , bx\n")
    else:
        dosya.write( "\tmov bx , %s\n"%(tok_list[index+1]))
        dosya.write( "\tsub ax , bx\n")


def assembly(yol, dosya_adi):
    k = dosya_oku(yol)
    tok_list = ayir(k)
    index = 0
    rstack = {}
    symbol_table = {}
    adres = 200
    dosya = open(dosya_adi, "w")
    dosya.write("\torg 100h\n")
    for i in tok_list:
        if i == 'load':
            loadla(tok_list, index, rstack, symbol_table, dosya)
        elif i == 'mul':
            mulla(tok_list, rstack, index, symbol_table, dosya)
        elif i == 'sta':
            rstack, symbol_table, adres = stala(tok_list, index, rstack, symbol_table, adres, dosya)
        elif i == 'mov':
            adres = movla(tok_list, index, rstack, symbol_table, adres, dosya)
        elif i == 'add':
            addle(tok_list, rstack, index, symbol_table, dosya)
        elif i == 'div':
            divle(tok_list, rstack, index, symbol_table, dosya)
        elif i == 'sub':
            subla(tok_list, rstack, index, symbol_table, dosya)
        else:
            if i == 'cmp':
                if tok_list[index+3] in symbol_table:
                    dosya.write( "\tcmp ax , [%s]\n"%(symbol_table[tok_list[index+3]]))
                else:
                    dosya.write( "\tcmp ax , %s\n"%(tok_list[index+3]))
            elif i[0:len(i)-2] == 'label':
                if tok_list[index+1] != 'nop':
                    dosya.write( i + "\n")
                else:
                    dosya.write( i + " nop\n")
            elif i == 'jump':
                dosya.write( "\tjmp " + tok_list[index+1] + "\n")
            elif i == 'jb' or i == 'ja' or i == 'je' or i == 'jbe' or i == 'jae' or i == 'jnz':
                dosya.write( "\t"+ i + " " + tok_list[index+1] + "\n")
            elif i == 'write':
                dosya.write( '\tmov ax , [%s]\n'%(symbol_table[tok_list[index+1]]))
                dosya.write("""\tcall print_ax     
\tmov ah, 1
\tint 21h        
\tret   
\tprint_ax proc
\tcmp ax, 0
\tjne print_ax_r
\tpush ax
\tmov al, '0'
\tmov ah, 0eh
\tint 10h
\tpop ax
\tret 
\tprint_ax_r:
\tpusha
\tmov dx, 0
\tcmp ax, 0
\tje pn_done
\tmov bx, 10
\tdiv bx    
\tcall print_ax_r
\tmov ax, dx
\tadd al, 30h
\tmov ah, 0eh
\tint 10h    
\tjmp pn_done
\tpn_done:
\tpopa  
\tret  
\tendp""")
                dosya.close()
                break
            elif i == 'hlt':
                dosya.write( "\tret\n")

        index = index + 1
    dosya.close()

