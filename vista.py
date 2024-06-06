import tkinter as tk
from tkinter import ttk
import customtkinter as ctk





class Principal:
    def __init__(self, root, matriz_precios, controlador):
        self.controlador = controlador
        self.root = root
        self.calidades = ['Eco.','Refor.']
        self.varAncho = tk.DoubleVar(value=1.0)
        self.varAlto = tk.DoubleVar(value=1.0)
        self.varCosto = tk.DoubleVar(value=0.0)
        self.columnas = ('Ancho','Alto','Eco.','Refor.')
        self.matriz_precios = matriz_precios
        
        self.frame = tk.Frame(self.root, bg='white')
        ### etiqueta de calcular costo y boton de precios #######
        self.labelCalcularCosto = tk.Label(self.frame, text='Calcular Costo', font='arial 18 bold', bg='white')
        self.labelCalcularCosto.place(anchor='center', rely=.05, relx=.35)
        self.botonPrecios = tk.Button(self.frame, text='Precios', font='arial 11 bold', command=self.controlador.mostrar_pantalla_precios)
        self.botonPrecios.place(anchor='ne', rely=.02, relx=.95)
        
        ### frame de entrada de datos para calcular costos #######
        self.frameCalcular = tk.Frame(self.frame, height=30, background='gray36')
        self.frameCalcular.place(anchor='n', rely= .12, relx=.5, relwidth=1, relheight=.35)

        self.etiquetaAncho = tk.Label(self.frameCalcular, text='Ancho:',font='arial 16 bold', background='gray36', fg='white').place(anchor='ne',relx=.25, rely=.15,)
        self.etiquetaAlto = tk.Label(self.frameCalcular, text='Alto:',font='arial 16 bold', background='gray36', fg='white').place(anchor='ne',relx=.25, rely=.6,)
        self.etiquetaCalidad = tk.Label(self.frameCalcular, text='Calidad:',font='arial 16 bold', background='gray36', fg='white').place(anchor='ne',relx=.87, rely=.15,)

        self.entryAncho = tk.Entry(self.frameCalcular, textvariable=self.varAncho, font='arial 14 bold', justify='right').place(anchor='nw', relx=.27, rely=.19, relwidth=.16, relheight=.14)
        self.entryAlto = tk.Entry(self.frameCalcular, textvariable=self.varAlto, font='arial 14 bold', justify='right').place(anchor='nw', relx=.27, rely=.64, relwidth=.16, relheight=.14)

        self.comboCalidad = ttk.Combobox(self.frameCalcular, values=self.calidades, font='arial 12 bold', state='readonly')
        self.comboCalidad.place(anchor='ne', relx=.85, rely=.4, relheight=.15, relwidth=.18)
        self.comboCalidad.set(self.calidades[0])

        ### etiqueta de costo y boton calcular  ####
        self.etiquetaCosto = tk.Label(self.frame, text='COSTO: $', font='arial 17 bold', bg='white').place(relx=.05, rely=.48)
        self.etiquetaValorCosto = tk.Label(self.frame, textvariable=self.varCosto, font='arial 17', anchor='w', bg='white')
        self.etiquetaValorCosto.place(anchor='nw', relx=.35, rely=.48, relwidth=.35)

        self.botonCalcular = tk.Button(self.frame, text='Calcular', font='arial 12 bold', command=self.controlador.calcular_costo)
        self.botonCalcular.place(anchor='ne', relx=.95, rely=.48)

        #### frame de espacio de separacion ####
        self.frameEspacio = tk.Frame(self.frame,  bg='gray36').place(anchor='center', relx=.5, rely=.57, relwidth=1, relheight=.02)
        #### medidas comunes   ####
        self.etiquetaMedidasComunes = tk.Label(self.frame, text='Medidas comunes:', font='arial 12 bold', bg='white').place(relx=.05, rely=.58)

        self.tablaPrecios = ttk.Treeview(self.frame, columns=self.columnas, show='headings')
        self.configurarTablaPrecios()
        self.tablaPrecios.place(anchor='n', relx=.5, rely=.64, relwidth=.95, relheight=.34)
        
    def mostrar(self):
        self.frame.pack(fill='both', expand=True)
    def ocultar(self):
        self.frame.forget()
    
    def get_datos_entrada(self):
        try:
            ancho = self.varAncho.get()
            alto = self.varAlto.get()
        except:
            ancho, alto = 0, 0
        
        calidad = 1 if self.comboCalidad.get() == 'Eco.' else 2
        return (ancho, alto, calidad)

    def mostrar_precio(self, precio):
        self.varCosto.set(value=precio)

    def configurarTablaPrecios(self):
        for col in self.columnas:
            self.tablaPrecios.heading(col, text=col)
            self.tablaPrecios.column(col, width=90)
        
        for fila in self.matriz_precios:
            self.tablaPrecios.insert('', tk.END, values=fila)

    



class Precios:
    def __init__(self, root, insumos_precios, controlador):
        self.root = root
        self.controlador = controlador
        self.insumos_precios = insumos_precios
        self.entries = []

        # frame principal
        self.frame = tk.Frame(self.root, bg='white')

        ## etiqueta de lista de precios y boton "volver" ###
        self.labelListaPrecios = tk.Label(self.frame, text='Lista de Precios', font='arial 18 bold', bg='white')
        self.labelListaPrecios.place(anchor='center', rely=.05, relx=.57)
        self.botonVolver = tk.Button(self.frame, text='Volver', font='arial 11 bold', command=self.controlador.mostrar_pantalla_principal)
        self.botonVolver.place(anchor='nw', rely=.02, relx=.05)

        ### rotulo de insumos "Insumo" "Precio" ###
        self.frameRotulo = tk.Frame(self.frame, bg='gray36')
        self.frameRotulo.place(anchor='n', rely=.12, relx=.5, relwidth=1, relheight=.05)
        self.labelRotulo = tk.Label(self.frameRotulo, text='Insumo                                         Precio', font='arial 11 bold', fg='white', bg='gray36')
        self.labelRotulo.place(anchor='n', rely=.1, relx=.5, relwidth=1)

        ### canvas de lista de precios ###
        self.canvas = tk.Canvas(self.frame, bg='white')
        self.canvas.place(anchor='n', rely=.17, relx=.5, relwidth=1, relheight=.7)
        self.scrollbar = ttk.Scrollbar(self.frame, orient='vertical', command=self.canvas.yview)
        self.scrollbar.place(anchor='ne', relx=1, rely=.17, relheight=.7)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.frame_in_canvas = tk.Frame(self.canvas, bg='white')
        self.canvas.create_window((0,0), window=self.frame_in_canvas, anchor='nw')
        self.frame_in_canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

        ## frame de separacion y boton de guardar cambios ###
        self.frameEspacio = tk.Frame(self.frame, bg='gray36').place(anchor='n', relx=.5, rely=.87, relwidth=1, relheight=.02)
        self.botonGuardar = tk.Button(self.frame, text='Guardar Cambios', font='arial 11 bold', command=self.controlador.guardar_precios)
        self.botonGuardar.place(anchor='n', rely=.915, relx=.5)




    def mostrar(self):
        self.frame.pack(fill='both', expand=True)

    def ocultar(self):
        self.frame.forget()

    def cargar_filas(self):
            self.entries = []  # Lista para almacenar referencias a los campos de entrada
            for i, (insumo, precio) in enumerate(self.insumos_precios):
                label = tk.Label(self.frame_in_canvas, text=insumo, font='arial 12', bg='white', width=20)
                label.grid(row=i, column=0, padx=10, pady=5, sticky='w')
                
                entry = tk.Entry(self.frame_in_canvas, font='arial 12', justify='right', width=14, bg='gray85')
                entry.insert(0, str(precio))  # Insertar el precio inicial en el campo de entrada
                entry.grid(row=i, column=1, padx=10, pady=5, sticky='e')
                
                self.entries.append(entry)
    
    def guardar_precios(self):
        l = self.insumos_precios
        for i in range(len(self.insumos_precios)):
            try:
                nuevo_precio = float( self.entries[i].get() )    
            except ValueError: continue
            l[i] = (l[i][0], nuevo_precio)

        self.insumos_precios = l
    
    def get_lista_precios(self):
        return self.insumos_precios



    def _on_mousewheel(self, event):
        if event.num == 5 or event.delta == -120:
            self.canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta == 120:
            self.canvas.yview_scroll(-1, "units")




