# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 16:47:14 2021

@author: Fernando
"""

import pandas as pd
import numpy as np

dirXML = "D:\\RCNN UA-DETRAC\\DETRAC-MOT-toolkit\\results\\GOG\\R-CNN\\0.1\\"
secuencia = "63563" # <------ Secuencia a procesar (video)

D = "Densidad_RCNN_" + secuencia + ".txt"
Y = "RCNN" + secuencia + ".txt"

dfD=pd.read_csv(D, sep=',',header=None)
dfY=pd.read_csv(Y, sep=',',header=None)

d=np.array(dfD.to_numpy())
y=np.array(dfY.to_numpy())
filas=np.shape(y)
fila=filas[0]
filasD=np.shape(d)
filaD=filasD[0]
#print(fila)
Frame = []
l_x = []
l_y = []
l_w = []
l_h = []
l_densidad=[]
for i in range(1,filaD):
    f=d[i][0]
    de=d[i][1]
    for j in range(0,fila):
        fr=y[j][0]
        x=y[j][1]
        yy=y[j][2]
        w=y[j][3]
        h=y[j][4]
        
        if(f == fr):
            Frame.append(fr)
            l_x.append(x)
            l_y.append(yy)
            l_w.append(w)
            l_h.append(h)
            l_densidad.append(de)
            
            
df = pd.DataFrame({'frame': Frame,
                    'x': l_x,
                   'y': l_y,
                   'w': l_w,
                   'h': l_h,
                   'densidad': l_densidad,
                   })
nombreArchivo = 'RCNN_RED_' + secuencia + '.txt'
df.to_csv(nombreArchivo, index=False)   
            
    
    
    
    
