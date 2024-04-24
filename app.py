import tkinter as tk


from modelo import conn, Ventana




class Inicio:

    def __init__(self, app):
        self.app = app
        self.root = tk.Tk()
        self.root.geometry('240x300+600+170')
        self.root.title('Inicio')

        self.fuente_botones = 'arial 15'
        self.ancho_botones = .65


        self.label_inicio = tk.Label(self.root,text='Inicio', font='arial 20 bold')    
        self.label_inicio.place(anchor='center', relx=.5, rely=.18)

        self.b_calcular = tk.Button(self.root, text='Calcular', font=self.fuente_botones, command=self.calcular)
        self.b_calcular.place(anchor='center', relx=.5, rely=.4, relwidth=self.ancho_botones)

        self.b_configurar = tk.Button(self.root, text='Configurar', font=self.fuente_botones, command=self.configurar)
        self.b_configurar.place(anchor='center', relx=.5, rely=.6, relwidth=self.ancho_botones)

        self.b_salir = tk.Button(self.root, text='Salir', font=self.fuente_botones, command=lambda : self.root.destroy())
        self.b_salir.place(anchor='center', relx=.5, rely=.8, relwidth=self.ancho_botones)

        self.root.mainloop()

    def calcular(self):
        self.root.destroy() 
        self.app.mostrar_calcular()
    
    def configurar(self):
        self.root.destroy()
        self.app.mostrar_configuraciones()



class Calcular_precio:
    
    def __init__(self, app):
        self.app = app
        self.root = tk.Tk()
        self.root.geometry('335x430+450+120')
        self.root.title('Calcular precio')

        self.fuente = 'arial 15'

        self.ancho = tk.DoubleVar(value=1.0)
        self.alto = tk.DoubleVar(value=1.0)
        self.nivel_calidad = tk.IntVar(value=1)
        self.precio = tk.DoubleVar(value=0.000)

        self.b_volver = tk.Button(self.root, text='volver', font='arial 13', command=self.volver)
        self.b_volver.place(relx=.03, rely=.03, relheight=.08, relwidth=.25)

        self.label_ancho = tk.Label(self.root, text='Ancho:', font=self.fuente)
        self.label_ancho.place(relx=.12, rely=.2, relheight=.1, relwidth=.25, anchor='w')
        self.label_alto = tk.Label(self.root, text='Alto:', font=self.fuente)
        self.label_alto.place(relx=.12, rely=.35, relheight=.1, relwidth=.25, anchor='w')
        self.label_n_c = tk.Label(self.root, text='Nivel/Calidad:', font=self.fuente)
        self.label_n_c.place(relx=.05, rely=.5, relheight=.1, relwidth=.35, anchor='w')

        self.in_ancho = tk.Entry(self.root, font=self.fuente, textvariable=self.ancho, justify='center')
        self.in_ancho.place(relx=.44, rely=.2, relheight=.07, relwidth=.3, anchor='w')
        self.in_alto = tk.Entry(self.root, font=self.fuente, textvariable=self.alto, justify='center')
        self.in_alto.place(relx=.44, rely=.35, relheight=.07, relwidth=.3, anchor='w')
        self.in_alto = tk.Entry(self.root, font=self.fuente, textvariable=self.nivel_calidad, justify='center')
        self.in_alto.place(relx=.44, rely=.5, relheight=.07, relwidth=.15, anchor='w')
        
        self.b_calcular = tk.Button(self.root, text='Calcular', font='arial 13', command=self.calcular_precio)
        self.b_calcular.place(anchor='center', relx=.5, rely=.75, relheight=.08, relwidth=.3)

        self.label_precio = tk.Label(self.root, text='Precio:', font=self.fuente)
        self.label_precio.place(anchor= 'center', rely=.85, relx=.3)
        self.label_precio = tk.Label(self.root, textvariable=self.precio, font=self.fuente)
        self.label_precio.place(anchor='center', rely=.85, relx=.6)

        self.root.mainloop()

    def volver(self):
        self.root.destroy()
        self.app.mostrar_inicio()
    
    def calcular_precio(self):
        try:
            ancho, alto, n_c = float(self.ancho.get()), float(self.alto.get()), int(self.nivel_calidad.get())
            ventana = Ventana(ancho, alto, n_c)
            precio = ventana.calcular_precio()
            self.precio.set(value=precio)
        except:
            ValueError

class Insumo:
    def __init__(self, master, registro_obeto):
        self.master = master

        nombre, n_c, metros, cantidad, precio = registro_obeto
        
        self.nombre = tk.StringVar(value=nombre)
        self.n_c = tk.StringVar(value=n_c) if n_c else tk.StringVar(value='---')
        self.metros = tk.StringVar(value=metros) if metros else tk.StringVar(value='---')
        self.cantidad = tk.StringVar(value=cantidad) if cantidad else tk.StringVar(value='---')
        self.precio  = tk.StringVar(value=precio) if precio else tk.StringVar(value='---')
        self.fuente = 'arial 11'

        self.frame = tk.Frame(self.master)
        self.frame.config(width=440, height=25)

        self.lab_nombre = tk.Label(self.frame, textvariable=self.nombre, font=self.fuente, justify='left')
        self.lab_nombre.place(anchor='w', rely=.5, relx=.0, relheight=.8, relwidth=.30)

        self.in_nivel_calidad = tk.Entry(self.frame, textvariable=self.n_c, state='disabled', font=self.fuente, justify='center')
        self.in_nivel_calidad.place(anchor='w', rely=.5, relx=.32, relheight=.8, relwidth=.07) 

        self.in_metros = tk.Entry(self.frame, textvariable=self.metros, state='disabled' if not metros else 'normal', font=self.fuente, justify='center')
        self.in_metros.place(anchor='w', rely=.5, relx=.41, relheight=.8, relwidth=.15)

        self.in_cantidad = tk.Entry(self.frame, textvariable=self.cantidad, state='disabled' if not cantidad else 'normal', font=self.fuente, justify='center')
        self.in_cantidad.place(anchor='w', rely=.5, relx=.58, relheight=.8, relwidth=.15)
        
        self.in_precio = tk.Entry(self.frame, textvariable=self.precio, font=self.fuente, justify='center')
        self.in_precio.place(anchor='w', rely=.5, relx=.75, relheight=.8, relwidth=.25)

        self.frame.pack()

    def guardar_datos(self):
        if 'p_' in self.nombre.get():
            conn.actualizar_perfil(self.nombre.get(), self.n_c.get(), self.metros.get(), self.precio.get())
        elif self.cantidad.get() != '---':
            conn.actualizar_por_cantidad(self.nombre.get(), self.cantidad.get(), self.precio.get())
        else:
            conn.actualizar_por_metros(self.nombre.get(), self.metros.get(), self.precio.get())


class Confguraciones:

    def __init__(self, app):
        self.app = app
        self.root = tk.Tk()
        self.root.geometry('460x630+450+100')
        self.root.title('Configurar Precios')

        self.lista_insumos = []

        self.b_volver = tk.Button(self.root, text='volver', font='arial 13', command=self.volver)
        self.b_volver.place(relx=.03, rely=.03, relheight=.04, relwidth=.2)

        self.lab_rotulo = tk.Label(self.root, text='Nombre           Calid.    Mts.       Cantid.        Precio($)', font='arial 12 bold')
        self.lab_rotulo.place(anchor='n', rely=.075, relx=.5, relheight=.05)

        self.insumos = tk.Frame(self.root)

        for registro in conn.obtener_tabla():
            self.lista_insumos.append( Insumo(self.insumos, registro) )

        self.insumos.place(rely=.13, relx=.5, relheight=.78, relwidth=.95, anchor='n')

        self.b_guradar = tk.Button(self.root, text='Guardar', font='arial 13', command=self.guardar_datos)
        self.b_guradar.place(anchor='center', relx=.5, rely=.93, relheight=.04, relwidth=.25)

        self.root.mainloop()

    def volver(self):
        self.root.destroy()
        self.app.mostrar_inicio()

    def guardar_datos(self):
        for insumo in self.lista_insumos:
            insumo.guardar_datos()
            
