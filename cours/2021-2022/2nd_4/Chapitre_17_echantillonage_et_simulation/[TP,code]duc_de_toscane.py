from lycee import *
def somme3d():
    return randint(1,6) + randint(1,6) + randint(1,6)

n=demande("Donner le nombre de lancers à effectuer:")
neuf=0
dix=0

for i in range(1,n+1):
    if somme3d()==9:
        neuf=neuf+1
    if somme3d()==10:
        dix=dix+1
    repere.plot(i,neuf/i,'gx')
    repere.plot(i,dix/i,'bx')

print("La fréquence de neuf obtenus est égale à :",neuf/n)
print("La fréquence de dix obtenus est égale à :",dix/n)
repere.axis([1,n,0,0.5])
repere.show()

