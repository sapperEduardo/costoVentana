import tkinter as tk

from modelo import Coneccion
from modelo import obtener_insumos
from modelo import Ventana
from vista import Principal, Precios


eco = lambda x, y: Ventana(x,y,1).calcularPrecio()
refor = lambda x, y: Ventana(x,y,2).calcularPrecio()

precios_ventanas_comunes = [
    (1,1,eco(1,1),refor(1,1)),
    (1.2,1,eco(1.2,1),refor(1.2,1)),
    (1,1.2,eco(1,1.2),refor(1,1.2)),
    (1.2,1.2,eco(1.2,1.2),refor(1.2,1.2)),
    (1.5,1,eco(1.5,1),refor(1.5,1)),
    (1.5,1.5,eco(1.5,1.5),refor(1.5,1.5)),
]

    



class Controlador:
    def __init__(self, root, precios_comunes):
        self.root = root
        self.precios_comunes = precios_comunes
        self.insumos = obtener_insumos()

        self.principal = Principal(root, self.precios_comunes, self)
        self.precios = Precios(self.root, self)

    
    def mostrar_pantalla_principal(self):
        self.precios.ocultar()
        self.principal.mostrar()

    def mostrar_pantalla_precios(self):
        self.principal.ocultar()
        self.precios.cargar_filas(self.insumos)
        self.precios.mostrar()

    def calcular_costo(self):
        ancho, alto, calidad = self.principal.get_datos_entrada()
        if ancho + alto != 0:
            precio = Ventana(ancho, alto, calidad).calcularPrecio()
            self.principal.mostrar_precio(precio)


    def guardar_precios(self):
        precios = self.precios.getPrecios()
        l = len(precios)
        for i in range(l):
            try:
                p = float(precios[i])
                self.insumos[i].actualizarPrecio(p)
            except: 
                continue
        Coneccion().guardar_datos()

    def actualizar_lista_precios_insumos(self):
        for insumo in obtener_insumos():
            insumo.cargarPrecio()



def main():
    ventana = tk.Tk()
    
    try: ventana.iconbitmap('_internal\\icono.ico')
    except: pass

    ventana.title('costoVentana')
    ventana.geometry('400x470')
    ventana.resizable(False,False)

    Ctr = Controlador(ventana, precios_ventanas_comunes)
    Ctr.mostrar_pantalla_principal()


    ventana.mainloop()



if __name__ == '__main__':  
    main()
