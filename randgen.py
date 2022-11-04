import random
def init_matrices():
    print("Enter weight dims(l,m) and the number of columns in input(n of (m,n))")
    l,m,n=[int(i) for i in input().split()]

    W=open("weightmat.txt","w")
    I=open("inputmat.txt","w")

    W.write(str(l)+" "+str(m)+"\n")
    for i in range(l):
        tmp=[str(random.uniform(0,1)) for j in range(m)]
        tm=" ".join(tmp)
        tm+="\n"
        W.write(tm)

    I.write(str(m)+" "+str(n)+"\n")
    for i in range(m):
        tmp=[str(random.uniform(0,1)) for j in range(n)]
        tm=" ".join(tmp)
        tm+="\n"
        I.write(tm)

    W.close()
    I.close()