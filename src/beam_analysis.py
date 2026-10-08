import matplotlib.pyplot as plt
import matplotlib.patches as mpath
import numpy as np

#L = [[x1,y1,x2,y2],[x1,y1,x2,y2]]
L = [[0,0,6,2],[2,2,4,6],[0,6,6,8]]
print(L)

def surface(x1,y1,x2,y2):
    h = abs(y2-y1)
    l = abs(x2-x1)
    return h*l

def cdg_mini(x1,y1,x2,y2):
    xg = x1 + abs(x1-x2)/2
    yg = y1 + abs(y1-y2)/2
    #print("cdg intermediaire est: ",xg," ", yg )
    return xg, yg

def draw(L):
    fig, ax = plt.subplots()
    for i in range(len(L)):
        x1 = L[i][0]
        y1 = L[i][1]
        x2 = L[i][2]
        y2 = L[i][3]
        
        l = abs(x2-x1)
        h = abs(y2-y1)
        
        rect = mpath.Rectangle((x1, y1), l, h, edgecolor = 'black', linewidth = 1.5)
        ax.add_patch(rect)
    plt.show()
        
draw(L)



def cdg(L):
    sum_cov_x = 0
    sum_cov_y = 0
    surf = 0
    for i in range(len(L)):
        xg, yg = cdg_mini(*L[i])
        
        sum_cov_x += xg*surface(*L[i])
        sum_cov_y += yg*surface(*L[i])
        
        surf += surface(*L[i])
        cdg_x = sum_cov_x/surf
        cdg_y = sum_cov_y/surf 
    return cdg_x, cdg_y

cdg_x, cdg_y = cdg(L)


print("le centre de gravite est: x=", cdg_x, " y=" ,cdg_y)

#
# Calcul du moment quadratique
#

def moment_quadratique_mini(x1,y1,x2,y2):
    h = abs(y2-y1)
    l = abs(x2-x1)
    Igx = (h**3*l)/12
    Igy = (h*l**3)/12
    return Igx, Igy

def moment_quadratique_tot(L):
    Igx_tot = 0
    Igy_tot = 0
    for i in range(len(L)):
        xg, yg = cdg_mini(*L[i])
        Igx, Igy = moment_quadratique_mini(*L[i])
        Igx_tot += Igx + (cdg_x - xg)**2 * surface(*L[i])
        Igy_tot += Igy + (cdg_y - yg)**2 * surface(*L[i])
    return Igx_tot, Igy_tot

Igx_tot, Igy_tot = moment_quadratique_tot(L)

print("le moment quadratique est: Igx= ", Igx_tot, " Igy= " ,Igy_tot)


#
# Calculs N , T et Mf
#
"""
def acquisition():
    L = input("La longeur de la poutre (m) ? .... ")
    Fx=[]
    Fy=[]
    while 1 != 0:
        fx=[]
        fy=[]
        a = input("Axe de la force : ")
        if a != '':
            if a.lower() == "x":
                fx.append(float(input('La valeur de la force (N) selon X : ')))
                fx.append(float(input('la position de la force (m) : ')))
                Fx.append(fx)
            elif a.lower() == "y":
                fy.append(float(input('La valeur de la force selon Y (N) : ')))
                fy.append(float(input('la position de la force (m) : ')))
                Fy.append(fy)
            else:
                print("Erreur")
        else:
            break               
    print (Fx, Fy)
    return Fx, Fy , L
        
Fx, Fy, L = acquisition()
"""



def Mf(Fy, L):
    B_len = np.linspace(0,L,100)
    Mf = np.zeros(len(B_len))
    #on trie Fy en fonction de la distance
    F = []
    while len(Fy) != 0:
        i_mini = 0
        for i in range(len(Fy)):
            if Fy[i][1] < Fy[i_mini][1]:
                i_mini = i
        F.append(Fy.pop(i_mini))
        
    #on caclule Mf   
    for i in range(len(Mf)):
        m = 0    
        for force in F:
            if force[1] < B_len[i]:
                m = m + force[0]*(B_len[i] - force[1])
        Mf[i] = m
                
    print(F)
    print(Mf)
    return Mf, B_len

Mf, B_len = Mf([ [10.0, 0.0], [-20.0, 5.0], [10.0, 10.0]], 10)


plt.plot(B_len, Mf)
plt.show()