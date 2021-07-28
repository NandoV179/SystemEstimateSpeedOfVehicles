# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 12:30:04 2021

@author: Fernando
"""


import pandas as pd
import numpy as np

# 1 Leer frames
# 2 Por cada frame a partir del segundo, calcular dx, dy, dw, dt
# 3 Construir tabla en archivo csv.
#   Por simplicidad, utilizaremos DataFrame de pandas

dirXML = "D:\\RCNN UA-DETRAC\\DETRAC-MOT-toolkit\\diferencia de frames\\"
secuencia = "63563" # <------ Secuencia a procesar (video)
archivo = "RCNN_Com_MVI_" + secuencia + ".txt"




df=pd.read_csv(archivo, sep=',',header=None)


matrix=np.array(pd.DataFrame(df).to_numpy())

#print(matrix)

l_ids = []
l_dx = []
l_dy = []
l_dw = []
l_dh = [] 
l_vel = [] # Lista de velocidades

matrixFinal=[]

filas = 1620
for i in range (1,filas):
    frame1=matrix[i][1]
    id1=matrix[i][2]
    x1=matrix[i][3]
    y1=matrix[i][4]
    w1=matrix[i][5]
    h1=matrix[i][6]
    velocidad=matrix[i][7]
    fr1=int(float(frame1))
    
    fr3 = fr1 + 1
    #print(frame1, id1, x1, y1, w1, h1, velocidad)
    
    
    for j in  range(1,filas):
        frame2=matrix[j][1]
        #print(frame2)
        fr2=int(float(frame2))
        id2=matrix[j][2]
        x2=matrix[j][3]
        y2=matrix[j][4]
        w2=matrix[j][5]
        h2=matrix[j][6]
        #print("\n")
        #print(x2)
        #print(frame2, id2, y2, w2, h2)
        
        

        if fr3 == fr2 and id1 == id2:
            #print(frame1, id1, x1, y1, w1, h1 )
            #print(frame2, id2, x2, y2, w2, h2 )
                  
            
            #diferencias para YOLO
            #dx= int(x2) - int(x1)
            #dy= int(y2) - int(y1)
            #dw= int(w2) - int(w1)
            #dh= int(h2) - int(h1)
            
            #diferencia para RCNN
            dx= float(x2) - float(x1)
            dy= float(y2) - float(y1)
            dw= float(w2) - float(w1)
            dh= float(h2) - float(h1)
            
            #l_ids.append(id2+'_'+str(i+1)+'-'+str(i))
            l_dx.append(dx)
            l_dy.append(dy)
            l_dw.append(dw)
            l_dh.append(dh)
            l_vel.append(velocidad)
            
            break
         
df = pd.DataFrame({'dx': l_dx,
                   'dy': l_dy,
                   'dw': l_dw,
                   'dh': l_dh,
                   'Velocidad': l_vel})
nombreArchivo = 'velocidad_RCNN_' + secuencia + '.txt'
df.to_csv(nombreArchivo, index=False)      


