from modelo import Coneccion
from modelo import obtener_insumos


insumos = obtener_insumos()



for i in insumos:
    nombre = i.getNombre()
    precio = i.getPrecio()
    print(f'{nombre}: {precio}')



