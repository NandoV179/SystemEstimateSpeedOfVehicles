# -*- coding: utf-8 -*-
"""
Created on Sun May 17 18:40:44 2020

@author: rigo_

"""

import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt 
import matplotlib.image as mpimg 
import matplotlib.patches as patches
import cv2
import math
import numpy as np

## Clases para el manejo de información de DETRAC

class Dibujante:
    """ Encargado de dibujar un frame y marcar los objetivos
    """           
    def __init__(self, dirIMG = "", secuencia = ""):
        """ Constructor
        """
        self.asignarSecuencia(dirIMG, secuencia)
    # end constructor
        
    def asignarSecuencia (self, dirIMG, secuencia):
        """
        Asigna una secuencia en los atributos de la clase

        Parameters
        ----------
        dirIMG : string
            Directorio con imágenes.
        secuencia : string
            Nombre de la secuencia.

        Returns
        -------
        None.

        """        
        dirSEC = dirIMG + "MVI_" + secuencia + "/"
        self.dirSEC = dirSEC
    # end asignarSecuencia
        
    def dibujar (self, lectorSecuencias, idFrame):
        """
        Dibujar la imagen y marca los objetivos

        Parameters
        ----------
        lectorSecuencias : Secuencia
            Procesador de archivo XML ya cargado.
        idFrame : int
            Id del frame a dibujar

        Returns
        -------
        None.

        """
        frameActual = lectorSecuencias.listaFrames[idFrame]
        numero = frameActual["num"]
        archivoIMG = self.dirSEC + "img%05d.jpg" % (numero)
        figure, ax = plt.subplots(1)
        img = mpimg.imread(archivoIMG)        

        ax.imshow(img)
        
        objetivos = frameActual["targetList"]
        self.marcarObjetivos (objetivos, ax)        
        self.marcarRegionesIgnoradas (lectorSecuencias.regionesIgnoradas, ax)
        
        plt.show()
    # end dibujar
        
    def marcarObjetivos (self, objetivos, ax):
        """
        Aumenta los objetivos en la figura

        Parameters
        ----------
        objetivos : List of Dictionaries
            Lista de diccionarios con los objetivos.
        ax : Axis
            Eje donde se debe dibujar.

        Returns
        -------
        None.

        """
        for objetivo in objetivos:
            height = objetivo["box"]["height"]
            left = objetivo["box"]["left"]
            top = objetivo["box"]["top"]
            width = objetivo["box"]["width"]
            objId = objetivo["id"]
            rect = patches.Rectangle((left,top),width,height, edgecolor='tomato', facecolor="none")
            ax.add_patch(rect)
            ax.text(left, top, objId, color="r")
    # end marcarObjetivos
            
    def marcarRegionesIgnoradas(self, regiones, ax):
        """
        Marca las regiones ignoradas

        Parameters
        ----------
        regiones : List of dictionaries
            Lista de diccionarios con regiones a eliminar.
        ax : Axis
            Ejes donde se desea dibujar.

        Returns
        -------
        None.

        """
        for region in regiones:
            height = region["height"]
            left = region["left"]
            top = region["top"]
            width = region["width"]
            rect = patches.Rectangle((left,top),width,height, edgecolor='w', facecolor="none")
            ax.add_patch(rect)
            
    # end margarRegionesIgnoradas
            
    def dibujarEjemplos (self, train_images, train_labels, target_label = 1, nCols = 5, verbose = True):
        """
        Dibuja ejemplos de una etiqueta en particular

        Parameters
        ----------
        train_images : array of images
            Conjunto con las imágenes
        train_labels : array of labels
            Arreglo con la etiqueta respectiva de cada imagen
        target_label : int, optional
            Label objetivo. The default is 1.
        nCols : int, optional
            Número de columnas a mostrar. The default is 5.
        verbose : Bool, optional
            Indica si se muestra el mensaje con el número de ejemplos encontrados. The default is True.

        Returns
        -------
        None.

        """
        # Buscar ejemplos positivos
        arr = np.array(train_labels)
        x = np.where(arr == target_label)
        x = x[0] # Si devuelve un resultado está en una tupla y se toma el primer elemento que corresponde a la primera variable analizada.
        if verbose:
            print("Ejemplos label = ", target_label, " ", len(x), " de ", len(train_labels), " ejemplos para entrenamiento.")
        
        self.dibujarEjemplosPosiciones(train_images, x, nCols)
    # end dibujarEjemplos

    def dibujarEjemplosPosiciones (self, train_images, posiciones, nCols = 5):
        nEjemplos = len(posiciones)
        if nEjemplos < nCols:
            nCols = nEjemplos
        nColumnas = nCols
        nFilas = math.ceil(nEjemplos/nColumnas)
        fig, axs = plt.subplots(nFilas, nColumnas, constrained_layout=False)
        # Dibujar primer ejemplo positivo
        c = 0
        for i in range(0, nFilas, 1):
          for j in range(0, nColumnas, 1):
            if c < nEjemplos:              
              img = train_images[posiciones[c]]        
              axs[i, j].imshow(img)
              c = c + 1
            else:
              axs[i, j].set_axis_off()        
        plt.show()   
    # end dibujarEjemplosPosiciones           
# end class Dibujante

class Secuencia:
    """ Clase para el manejo de datos de DETRAC.
    """
    
    def archivoXML (self, dirXML, secuencia):
        """
        Genera el nombre del archivo XML

        Parameters
        ----------
        dirXML : string
            Directorio con archivos XML.
        secuencia : string
            Nombre de la secuencia.

        Returns
        -------
        archivoXML : string
            Ruta del archivo xml que corresponde a la secuencia.

        """
        archivoXML = dirXML + "MVI_" + secuencia + "_v3.xml"
        return archivoXML
    
    def buscarId (self, frame, id):
        """
        Busca un id dentro de un frame

        Parameters
        ----------
        frame : Dictionary
            Frame en el que se está buscando.
        id : int
            Id que se está buscando

        Returns
        -------
        None si no existe el id
        En caso contrario devuelve los datos del objeto con ese id

        """
        lista = frame["targetList"]
        res = None
        for actual in lista:
            if actual['id'] == id:
                res = actual
        return res
    
    def extraerFrame (self, imagen):
        """
        Extrae los datos de un frame (imagen)

        Parameters
        ----------
        imagen : frame de un XML
            Contiene las anotaciones por frame.

        Returns
        -------
        datosFrame : diccionario
            Datos del frame.

        """
        datosFrame = {
            "density": int(imagen.get("density")),
            "num": int(imagen.get("num"))
            }
        targetList = imagen.find("target_list")
        lista = []
        for target in targetList:
            caja = target.find("box")
            atributos = target.find("attribute")            
            listaOclusiones = self.extraerOclusiones(target)            
            datos = {
                "id": target.get("id"),
                "color": atributos.get("color"),
                "orientation": atributos.get("orientation"),
                "speed": atributos.get("speed"),
                "trajectory_length": atributos.get("trajectory_length"),
                "truncation_ratio": atributos.get("truncation_ratio"),
                "vehicle_type": atributos.get("vehicle_type"),
                "box": {
                    "height": float(caja.get("height")),
                    "left": float(caja.get("left")),
                    "top": float(caja.get("top")),
                    "width": float(caja.get("width"))
                    },
                "occlusion": listaOclusiones
                }                
            lista.append(datos)
        datosFrame["targetList"] = lista            
        return datosFrame
    
    def extraerOclusiones (self, target):
        """
        Extrae las oclusiones y las almacena en una lista

        Parameters
        ----------
        target : XML Element
            Target in XML

        Returns
        -------
        listaOclusiones : list
            Lista de oclusiones por defecto vacía.

        """
        listaOclusiones = []
        oclusiones = target.find("occlusion")
        if not(oclusiones is None):
            for region in oclusiones:
                datos = {
                    "height": region.get("height"),
                    "left": region.get("left"),
                    "occlusion_id": region.get("occlusion_id"),
                    "occlusion_status": region.get("occlusion_status"),
                    "top": region.get("top"),
                    "width": region.get("width"),
                         }
                listaOclusiones.append(datos)
        return listaOclusiones
    
    def getNumeroFrames (self):
        """
        Devuelve el número de frames

        Returns
        -------
        int
            Número de frames.

        """
        return len(self.listaFrames)
    # end getNumeroFrames
    
    def procesar (self, rutaArchivoXML):
        """Procesa un archivo XML de una secuencia de video 
        """
        self.tree = ET.parse(rutaArchivoXML)
        self.root = self.tree.getroot()
        
        # Información de la secuencia
        self.name = self.root.get("name")
        seq_at = self.root.find("sequence_attribute")
        self.camera_state = seq_at.get("camera_state")
        self.sence_weather = seq_at.get("sence_weather")
        
        self.procesarRegionesIgnoradas()
        self.procesarFrames()
    # end procesar

    def procesarFrames(self):
        """Extrae la información de los frames
        """
        lstFrames = self.root.findall("frame")
        self.listaFrames = []
        for imagen in lstFrames:
            nuevoFrame = self.extraerFrame(imagen)
            self.listaFrames.append(nuevoFrame)
    # end procesarFrames
    
    def procesarRegionesIgnoradas(self):
        """Extrae las regiones ignoradas en una lista
        """
        ign_reg = self.root.find("ignored_region")
        self.regionesIgnoradas = []
        for region in ign_reg:
            resRegion = {
                "height":float(region.get("height")),
                "left": float(region.get("left")),
                "top": float(region.get("top")),
                "width": float(region.get("width"))
                }
            self.regionesIgnoradas.append(resRegion)
    # end procesarRegionesIgnoradas
                
# end class Secuencia

class RCNN(Dibujante):
    """ Region - Convolutional Neural Network 
    """
    
    def __init__(self, dirIMG):
        """
        Constructor
        
        Returns
        -------
        None.

        """      
        # Número de candidatos
        self.maxNumCandidatos = 2000
        
        # Máximo número de ejemplos positivos
        self.maxPositivos = 40
        # Máximo número de ejemplos negativos
        self.maxNegativos = 40
        
        # Número máximo de ejemplos por etiqueta
        self.maxEtiqueta = 5 # Es pequeño por que en el video aparecerán muchos más
        
        # Umbral iou
        self.umbralIoUPositivo = 0.75 # Por defecto 0.7
        self.umbralIoUNegativo = 1 - self.umbralIoUPositivo
        
        # Ajustar ejemplos al tamaño especifico
        self.tamEjemplos = (227, 227)
        
        # Borde extra
        self.bordeExtra = 4
        
        # Selective search from OpenCV (cv2)
        # Asistente de búsqueda (Selective Search)
        self.ss = cv2.ximgproc.segmentation.createSelectiveSearchSegmentation()

        # Directorio de imágenes
        self.dirIMG = dirIMG
    # end constructor
        
    def archivoFrame(self, frameActual, secuencia):
        """
        Devuelve el archivo imagen del frame actual

        Parameters
        ----------
        frameActual : dictionary
            Información XML.
        secuencia : string
            Nombre de la secuencia.

        Returns
        -------
        archivoIMG : string
            Ruta al rchivo imagen correspondiente.

        """
        self.asignarSecuencia(secuencia) # Crea el directorio donde encuentra las imágenes dirSEC
        numero = frameActual["num"]
        archivoIMG = self.dirSEC + "img%05d.jpg" % (numero)
        return archivoIMG
    # end archivoFrame
        
    def asignarSecuencia(self, secuencia):
        """
        Asigna el directorio de imágenes respectivo a la secuencia

        Parameters
        ----------
        secuencia : string
            Nombre de la secuencia.

        Returns
        -------
        None.

        """
        super().asignarSecuencia(self.dirIMG, secuencia)
    # end asignarSecuencia
  
    def aumentarEjemplo(self, imout, x, y, w, h, etiqueta):
        """
        Aumenta un ejemplo den las lista de entrenamiento

        Parameters
        ----------
        imout : Image
            Imagen que se está procesando.
        x : number
            Coordenada en x.
        y : number
            Coordenada en y.
        w : number
            Ancho del ejemplo.
        h : number
            Alto del ejemplo.
        etiqueta : int
            Etiqueta por el momento positivo o negativo (1, 0).

        Returns
        -------
        res: Boolean
            True if there is no error.

        """
        width, height = self.tamanoImagen(imout)
        (x1, x2) = self.aumentarSeparacion (x, self.bordeExtra, w + self.bordeExtra, 0, width-1)
        (y1, y2) = self.aumentarSeparacion (y, self.bordeExtra, h + self.bordeExtra, 0, height-1)
                
        
        timage = imout[y1:y2,x1:x2]
        wRegion, hRegion = self.tamanoImagen(timage)
        if wRegion > 0 and hRegion > 0:
            resized = cv2.resize(timage, self.tamEjemplos, interpolation = cv2.INTER_AREA)
            self.train_images.append(resized)
            self.train_labels.append(etiqueta) # Etiqueta del ejemplo
            return True
        return False
    # end aumentarEjemplo
        
    def aumentarSeparacion (self, z, decremento, incremento, umbralDesde, umbralHasta):
        """
        Genera los decrementos e incrementos respetando los umbrales.

        Parameters
        ----------
        z : number
            Número original.
        decremento : number
            Número a restar.
        incremento : number
            Número a aumentar.
        umbralDesde : number
            Umbral inferior.
        umbralHasta : number
            Umbral superior.

        Returns
        -------
        z1 : number
            z - decremento.
        z2 : number
            z + decremento.

        """
        z1 = z - decremento
        if z1 < umbralDesde:
            z1 = umbralDesde
        z2 = z + incremento
        if z2 > umbralHasta:
            z2 = umbralHasta
        return (z1, z2)
    
    def balancearEjemplos(self, train_labels):
        """
        Devuelve las posiciones de positivos y negativos
        balanceando el número de ejemplos

        Parameters
        ----------
        train_labels : List
            Lista de etiquetas.

        Returns
        -------
        positivos : Array
            Arreglo con posiciones de ejemplos positivos.
        negativos : Array
            Arreglo con posiciones de ejemplos negativos.

        """
        arr = np.array(train_labels)
        x = np.where(arr == 1) # Ejemplos positivos
        positivos = x[0]
        x = np.where(arr == 0) # Ejemplos negativos
        negativos = x[0]
        
        nPositivos = len(positivos)
        nNegativos = len(negativos)
        
        if nNegativos > nPositivos:
            mayor = negativos
            menor = positivos
        else:
            mayor = positivos
            menor = negativos
        
        nMayor = len(mayor)
        nMenor = len(menor)    
        # Tomar muestra de negativos
        paso = int(nMayor / nMenor)
        sel = []
        for i in range (nMenor):
            sel.append(mayor[i*paso])
        
        if nNegativos > nPositivos:
            negativos = np.array(sel)
        else:
            positivos = np.array(sel)
        return (positivos, negativos)
    # balancear ejemplos
    
    def estaEnRegionIgnorada (self, candidato, listaRegionesIgnorar):
        """
        Revisa si el candidato está en alguna de las regiones a ignorar

        Parameters
        ----------
        candidato : Vector
            Position and size.
        listaRegionesIgnorar : List
            Lista de Coordendas de las regiones a ignorar

        Returns
        -------
        True or False.

        """
        for region in listaRegionesIgnorar:
            iou = self.get_iou(region, candidato)
            if iou >= self.umbralIoUPositivo:
                return True
        return False
    # estaEnRegionIgnorada
    
    def generarCoordenadasObjetivos(self, objetivos):
        """
        Genera la lista de coordenadas dado el diccionario de objetivos.

        Parameters
        ----------
        objetivos : Dictionary
            Diccionario generado de los archivos XML.

        Returns
        -------
        lista : list
            Lista de coordenadas x1, x2, y1, y2.

        """
        lista = []
        for objetivo in objetivos:
            height = objetivo["box"]["height"]
            left = objetivo["box"]["left"]
            top = objetivo["box"]["top"]
            width = objetivo["box"]["width"]
            #objId = objetivo["id"]
            lista.append({"x1":left, "x2":left + width, "y1":top, "y2":top+height})
        return lista
    # end generarCoordenadasObjetivos
    
    def generarCoordenadasRegionesIgnorar(self, lectorSecuencias):
        """
        Genera las coordenadas de las regiones a ignorar

        Parameters
        ----------
        lectorSecuencias : Secuencia
            Información del archivo XML.

        Returns
        -------
        lista : List
            Lista de coordenadas de las regiones ignoradas.

        """
        lista = []
        for region in lectorSecuencias.regionesIgnoradas:
            height = region["height"]
            left = region["left"]
            top = region["top"]
            width = region["width"]            
            lista.append({"x1":left, "x2":left + width, "y1":top, "y2":top+height})
        return lista
    # end generarCoordenadasRegionesIgnorar
    
    def generarEjemplosEntrenamiento(self, lectorSecuencias, idFrame, secuencia):        
        """
        Genera los ejemplos de entrenamiento

        Parameters
        ----------
        lectorSecuencias : Secuencia
            Tiene la información del XML.
        idFrame : int
            Id del frame a procesar.
        secuencia : String
            Nombre del secuencia.

        Returns
        -------
        list
            Lista de imágenes.
        List
            Lista de etiquetas.

        """
        
        frameActual = lectorSecuencias.listaFrames[idFrame]
        (archivoIMG, listaCoordenadas) = self.prepararDatos(frameActual, secuencia)
        # Revisar si esto se puede hacer una sola vez para todas las imágenes de la secuencia
        listaRegionesIgnorar = self.generarCoordenadasRegionesIgnorar (lectorSecuencias)
        
        # Leer imagen        
        image = cv2.imread(archivoIMG)
        
        # Ejecutar selective search
        self.ss.setBaseImage(image)
        self.ss.switchToSelectiveSearchQuality()
        #self.ss.switchToSelectiveSearchFast()
        ssresults = self.ss.process()

        # ---------------------------------
        # Preparar datos de entrenamiento
        # A partir de la búsqueda "SelectiveSearch"
        # ---------------------------------
        imout = image.copy()
        counter = 0
        falsecounter = 0
        contador ={} # Contador por ejemplo
        
        # Ejemplos de entrenamiento
        self.train_images=[]
        # Etiquetas
        self.train_labels=[]
                        
        # Revisar cada candidato
        for e,result in enumerate(ssresults):
            if ((counter >= self.maxPositivos) and (falsecounter >= self.maxNegativos) ) or (e >= self.maxNumCandidatos):
                break
            x,y,w,h = result
            candidato = {"x1":x,"x2":x+w,"y1":y,"y2":y+h}
            if (not self.estaEnRegionIgnorada(candidato, listaRegionesIgnorar)):
                # Comparar con etiquetas                
                for etiquetado in listaCoordenadas:
                    keyEtiquetado = frozenset(etiquetado.items())
                    if not(keyEtiquetado in contador): # Inicializa contador por etiquetas
                        contador[keyEtiquetado] = 0
                    # end if
                    iou = self.get_iou(etiquetado, candidato)
                    if (iou >= self.umbralIoUPositivo) and (contador[keyEtiquetado] < self.maxEtiqueta) and (counter < self.maxPositivos): # Porcentaje de traslape
                        if  self.aumentarEjemplo(imout, x, y, w, h, 1):
                            counter += 1
                            contador[keyEtiquetado] = contador[keyEtiquetado] + 1 
                    elif (iou < self.umbralIoUNegativo) and (falsecounter < self.maxNegativos):
                        if self.aumentarEjemplo(imout, x, y, w, h, 0):
                            falsecounter += 1
                    if (counter >= self.maxPositivos) and (falsecounter >= self.maxNegativos):
                        break
        return (self.train_images, self.train_labels)
    # end generarEjemplosEntrenamiento
    
    def get_iou(self, bb1, bb2):
        """ Calcula el índice de área de intersección entre la unión de dos 
            regiones.
        """    
        # Assert revisa condición, si no se cumple, dispara excepción.
        # x1 debe ser menor que x2, etc.
        assert bb1['x1'] < bb1['x2']
        assert bb1['y1'] < bb1['y2']
        assert bb2['x1'] < bb2['x2']
        assert bb2['y1'] < bb2['y2']    
        
        # Obtiene puntos extremos
        x_left = max(bb1['x1'], bb2['x1'])
        y_top = max(bb1['y1'], bb2['y1'])
        x_right = min(bb1['x2'], bb2['x2'])
        y_bottom = min(bb1['y2'], bb2['y2'])
        
        # Revisar si los puntos extremos no cumplen  x2 > x1
        if x_right < x_left or y_bottom < y_top:
            return 0.0    
        
        # Area de la intersección
        intersection_area = (x_right - x_left) * (y_bottom - y_top)    
        
        # Areas independientes
        bb1_area = (bb1['x2'] - bb1['x1']) * (bb1['y2'] - bb1['y1'])
        bb2_area = (bb2['x2'] - bb2['x1']) * (bb2['y2'] - bb2['y1'])
        
        # Área de la interesacción dividida por el área que no está en la inter-
        # sección.
        iou = intersection_area / float(bb1_area + bb2_area - intersection_area)
    
        # iou debe estar entre 0 y 1
        assert iou >= 0.0
        assert iou <= 1.0
    
        # retorna iou
        return iou

    def prepararDatos (self, frameActual, secuencia):
        """
        Preparar los datos, devuelve el nombre del archivo y una lista
        de las posiciones x1, y1, x2, y2

        Parameters
        ----------
        frameActual : TYPE
            DESCRIPTION.

        Returns
        -------
        (archivoIMG, listaCoordenadas).

        """
        archivoIMG = self.archivoFrame(frameActual, secuencia)
        
        objetivos = frameActual["targetList"]
        listaCoordenadas = self.generarCoordenadasObjetivos (objetivos)
        return (archivoIMG, listaCoordenadas)                
    # end dibujar

    def tamanoImagen (self, imagen):
        """
        Devuelve el tamaño de una imagen

        Parameters
        ----------
        imagen : Image
            Imagen almacenada en un arreglo generalmente de 3 dimensiones.

        Returns
        -------
        width : number
            Número de columnas.
        height : number
            Número de filas.

        """
        height = len(imagen)
        if height > 0:
            width = len(imagen[0])
        else:
            width = 0
        return (width, height)
# end class