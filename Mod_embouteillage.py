#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 13:40:59 2019

@author: Abdelmajid
"""

from tkinter import *
from random import *
import matplotlib.pyplot as plt
from time import *

# Paramètres
largeur = 1000
hauteur = 700
n=1
lim_x = int(largeur * 0.90)
x0, y0 = 100, 100
dt = 1
vx = 5


tau = 50
V0=0.5
a=0.08
d=10

#On définit les classes que l'on va utiliser

class Voiture:
    def __init__(self, x, y, taillex, tailley, canvas):
        self.x = x
        self.y = y
        self.taillex = taillex
        self.tailley = tailley
        
        # tkinter
        self.canvas = canvas
        self.rect = canvas.create_rectangle(x, y, x + taillex, y + tailley, width = 2, fill = "red")
    
    def deplacer(self, x, y):
        self.x = x
        self.y = y
        self.actualiser()
        
    def deplacer_delta(self, dx, dy):
        self.deplacer(self.x + dx, self.y + dy)
    
    def actualiser(self):
        self.canvas.coords(self.rect, self.x, self.y, self.x + self.taillex, self.y + self.tailley)
    
    def supprimer(self):
        self.canvas.delete(self.rect)
        del(self)
        
        
#Procédure 

root = Tk()
canvas = Canvas(root, width = largeur, height = hauteur, background='white')
canvas.pack(fill = "both", expand = True)


bar = canvas.create_rectangle(0, 0, 15, 10, width = 2, fill = 'red')

V = []

def generer(n, V):
    for i in range(n):
        p=len(V)
        if p==0:
            V.append(Voiture(x0, y0 + i*50, 4, 2, canvas))      #Première voiture(plus grosse pour mieux la vor)
        elif V[p-1].x>x0+10:
            V.append(Voiture(x0, y0 + i*50, 2, 1, canvas))
    canvas.after(tau, generer, n, V)                            #toujours dans la même liste, on y a donc accès



def deplacer(V):                                                #On définit la fonction qui va déplacer les voitures
    
    for v in V:
        i=V.index(v)
        if v.x + vx*dt >= lim_x:                                #Si la voiture sort de l'écran, on la supprime
            v.supprimer()
            del(V[0])
            continue
        if i==0:                                                #Pour la première voiture on crée la perturbation(ralentissement)
            if v.x>largeur/3 and v.x<2*largeur/3:
                v.deplacer_delta(2*dt/5,0)
            else:
                v.deplacer_delta(vx*dt, 0)
            continue
            
        else:                                                   #Utilisation de l'équation pour les voiture suivante
            l=a*(V[i-1].x-v.x)
            
            v.deplacer_delta(dt*l,0)
            continue
            
        
    canvas.after(dt, deplacer, V)
    
    




m=[]
t=[]
def bouchon(V, m, canvas, bar, t):                              #Crée une liste des voitures pris dans l'embouteillage
    p=len(V)
    l=[]
    for i in range(1, len(V)):
        if V[i - 1].x - V[i].x < d:
            l.append(V[i].x)
        
    if len(l)>3:                                                #Mesure du centre de gravité de l'embouteillage
        t.append(time())
        s = 1./len(l) * sum([x for x in l])
        m.append(s)
        canvas.coords(bar, s, y0 + 50, s + 15, y0 + 50 + 10)
        
        
    canvas.after(dt, bouchon, V, m, canvas, bar, t)     


#Lancement de la procédure

def close_window():
    root.destroy()

button =Button(text = "Click and Quit", 
                   command = close_window)
button.pack()

generer(n, V)
deplacer(V)
bouchon(V, m, canvas, bar, t)
root.mainloop()

#Apparation des mesures


plt.plot(m)
plt.show()
print(t[len(t)-1]-t[0])
print(m[len(m)-1])





