import matplotlib.pyplot as plt

def f(x):
    return(x**2-3*x+1)

def graphe(g,a,b,N):
    lx = [a+i*(b-a)/N for i in range(N+1)]
    ly = [g(x) for x in lx]
    print(lx)
    print(ly)
    plt.plot(lx,ly)
    plt.show()

graphe(f,-3,5,8)




