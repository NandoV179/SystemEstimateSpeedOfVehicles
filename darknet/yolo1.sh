#!/bin/bash

extencion=".jpg"
ruta=/home/nando/darknet/data/DETRAC-train-data/Insight-MVT_Annotation_Train/MVI_40981

for((i=100;i<=100;i++))
do
  if [ $i -le 9 ] 
  then
    ./darknet detect cfg/yolov3.cfg yolov3.weights $ruta/img0000$i$extencion $i
    
  elif [[ $i -ge 10 ]] && [[ $i -le 99 ]]
  then
	  ./darknet detect cfg/yolov3.cfg yolov3.weights $ruta/img000$i$extencion $i

  elif [[ $i -ge 100 ]] && [[ $i -le 999 ]]
  then
    ./darknet detect cfg/yolov3.cfg yolov3.weights $ruta/img00$i$extencion $i

  elif [ $i -ge 1000 ]
  then
    ./darknet detect cfg/yolov3.cfg yolov3.weights $ruta/img0$i$extencion $i

  else
    break 
  fi
done
