# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 20:54:45 2021

@author: Fernando
"""

import pandas as pd
import numpy as np

dirXML = "D:\\RCNN UA-DETRAC\\DETRAC-MOT-toolkit\\results\\GOG\\R-CNN\\0.1\\"
secuencia = "40141" # <------ Secuencia a procesar (video)
H = "MVI_" + secuencia + "_H.txt"
X = "MVI_" + secuencia + "_LX.txt"
Y = "MVI_" + secuencia + "_LY.txt"
W = "MVI_" + secuencia + "_W.txt"

dfH=pd.read_csv(H, sep=',',header=None)
dfX=pd.read_csv(X, sep=',',header=None)
dfY=pd.read_csv(Y, sep=',',header=None)
dfW=pd.read_csv(W, sep=',',header=None)

#print(dfH)
#print("\n")
#print(dfX)
#print("\n")
#print(dfY)
#print("\n")
#print(dfW)


x=np.array(dfX.to_numpy())
y=np.array(dfY.to_numpy())
w=np.array(dfW.to_numpy())
h=np.array(dfH.to_numpy())

#print("x")
#print(x)
#print("y")
#print(y)
##print("w")
#print(w)
#print("x")
#print(h)


filas= np.shape(h)
fila=filas[0]
columnas=np.shape(h)
columna=columnas[1]

#print(fila , columna)

Frames = []
l_x = []
l_y = []
l_w = []
l_h = []
l_densidad=[]
l_fr=[]
 
for i in range (0,fila):
    densidad=0
    for j in range (0,columna):
        mx=x[i][j]
        my=y[i][j]
        mw=w[i][j]
        mh=h[i][j]
        
        check=int(mx)
        
        if(check != 0):
            #print(mx, my, mw, mh,i)
            
            Frames.append(i+1)
            l_x.append(mx)
            l_y.append(my)
            l_w.append(mw)
            l_h.append(mh)
            #print(densidad)
            densidad = densidad +1
    
    l_densidad.append(densidad)
    l_fr.append(i+1)
        
        
            
        
df = pd.DataFrame({'frame': Frames,
                   'X': l_x,
                   'Y': l_y,
                   'W': l_w,
                   'H': l_h,
                   })
nombreArchivo = 'RCNN' + secuencia + '.txt'
df.to_csv(nombreArchivo, index=False)
 
df1 = pd.DataFrame({'frame': l_fr,
                   'densidad':l_densidad,
                   })
nombreArchivo1 = 'Densidad_RCNN_' + secuencia + '.txt'
df1.to_csv(nombreArchivo1, index=False)







