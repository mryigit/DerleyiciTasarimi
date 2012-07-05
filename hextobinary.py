karsilik={'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'A':10,'B':11,'C':12,'D':13,'E':14,'F':15}
def dosya_oku(dosya_adi):
    f = open(dosya_adi , "r")
    tok_list = []
    for i in f.read().split('\n'):
        tok_list.append(i.split(" "))
    f.close()
    return tok_list

def hex2dec(t):
    top=0
    j=0
    for i in range(len(t)-1,-1,-1):
        ek=karsilik[t[i]]
        top=top+(ek*(16**j))
        j=j+1
    return top
        
donusum="0123456789ABCDEF"
def dec2bin(n,taban):
    if n<taban:
        return donusum[n]
    else :
        return dec2bin(n/taban,taban)+donusum[n%taban]

def hextobinary(yol , dosya_adi):
    liste=dosya_oku(yol)
    dosya=open(dosya_adi, "w")
    for i in liste:
        for t in i:
            a=dec2bin(hex2dec(t),2)
            uzunluk=len(a)
            
            while uzunluk<8:
                a="0"+a
                uzunluk=uzunluk+1
                
                
            dosya.write(a+"\t")
        dosya.write("\n")
    dosya.close()

            
    
    
    
    
    
