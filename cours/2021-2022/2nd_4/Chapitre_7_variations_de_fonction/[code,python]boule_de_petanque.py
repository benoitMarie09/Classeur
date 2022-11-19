def f(x) :
    return(-0.25*x**2+1.4*x+0.6)

x=0
max=f(0)
xatteint=0

while x<=6:
    if f(x)>max:
        max = f(x)
        xatteint=x
    x = x + 0.01

print("La hauteur maximale atteinte est de ",max," mètres")
print("Elle est atteinte pour x = ",xatteint)



