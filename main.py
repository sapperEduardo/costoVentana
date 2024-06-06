import tkinter as tk
from modelo import obtener_lista_precios, guardar_precios
from modelo import Ventana
from vista import Principal, Precios


eco = lambda x, y: Ventana(x,y,1).calcularPrecio()
refor = lambda x, y: Ventana(x,y,2).calcularPrecio()

precios_comunes = [
    (1,1,eco(1,1),refor(1,1)),
    (1.2,1,eco(1.2,1),refor(1.2,1)),
    (1,1.2,eco(1,1.2),refor(1,1.2)),
    (1.2,1.2,eco(1.2,1.2),refor(1.2,1.2)),
    (1.5,1,eco(1.5,1),refor(1.5,1)),
    (1.5,1.5,eco(1.5,1.5),refor(1.5,1.5)),
]

insumos_precios = obtener_lista_precios()


class Controlador:
    def __init__(self, root, matriz_precios):
        self.root = root
        self.matriz_precios = matriz_precios

        self.principal = Principal(root, self.matriz_precios, self)
        self.precios = Precios(self.root, insumos_precios, self)


    
    def mostrar_pantalla_principal(self):
        self.precios.ocultar()
        self.principal.mostrar()

    def mostrar_pantalla_precios(self):
        self.principal.ocultar()
        self.precios.cargar_filas()
        self.precios.mostrar()

    def calcular_costo(self):
        ancho, alto, calidad = self.principal.get_datos_entrada()
        if ancho + alto != 0:
            precio = Ventana(ancho, alto, calidad).calcularPrecio()
            self.principal.mostrar_precio(precio)


    def guardar_precios(self):
        self.precios.guardar_precios()
        l = self.precios.get_lista_precios()
        guardar_precios(l)




def main():
    ventana = tk.Tk()
    ventana.iconbitmap('C:\\Users\\sebas\\OneDrive\\Documentos\\desk_venv\\Proyects\\costoVentana\\icono.ico')
    ventana.title('costoVentana')
    ventana.geometry('400x470')
    ventana.resizable(False,False)

    Ctr = Controlador(ventana, precios_comunes)
    Ctr.mostrar_pantalla_principal()


    ventana.mainloop()



if __name__ == '__main__':  
    main()
