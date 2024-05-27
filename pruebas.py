import json 


def cargar_datos():
    with open('datos.json', 'r') as f:
        return json.load(f)

Datos = cargar_datos()


def precio(codigo):
    global Datos
    for insumo in Datos["insumos"]:
        if codigo == insumo["codigo"]:
            print( insumo["precio"] )
        

precio(202)









