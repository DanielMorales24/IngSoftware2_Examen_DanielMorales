import customtkinter as ctk
from tkinter import messagebox, ttk
import pyodbc
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as patches
from datetime import datetime
import string

# Configuración de apariencia
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class SistemaBoletos:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Boletos - Examen")
        self.root.geometry("1100x750")
        
        # Conexión a la base de datos
        self.server = r"DELL_LAPTOP_DM\SQLDEVELOPER"
        self.database = "SistemaBoletos"
        self.conn = self.connect_to_db()
        
        # Variables de estado
        self.usuario_actual = None
        self.funcion_seleccionada = None
        self.asientos_seleccionados = []
        
        # Crear todos los frames
        self.crear_frames()
        
        # Mostrar pantalla inicial
        self.mostrar_pantalla_inicio()

    def connect_to_db(self):
        try:
            conn_str = (
                rf"DRIVER={{ODBC Driver 17 for SQL Server}};"
                rf"SERVER={self.server};"
                rf"DATABASE={self.database};"
                r"Trusted_Connection=yes;"
            )
            conn = pyodbc.connect(conn_str)
            return conn
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar a la base de datos:\n{str(e)}")
            return None

    def crear_frames(self):
        # Frame principal que contendrá todos los demás
        self.main_container = ctk.CTkFrame(self.root)
        self.main_container.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Frame de inicio (logo y botones)
        self.frame_inicio = ctk.CTkFrame(self.main_container, fg_color="transparent")
        
        # Logo y título
        ctk.CTkLabel(
            self.frame_inicio, 
            text="Examen - Gestion de Boletos", 
            font=("Arial", 32, "bold"),
            text_color="#1e88e5"
        ).pack(pady=(20, 40))
        
        # Botones principales
        ctk.CTkButton(
            self.frame_inicio,
            text="Iniciar Sesión",
            command=self.mostrar_login,
            width=220,
            height=50,
            font=("Arial", 16),
            corner_radius=10
        ).pack(pady=15)
        
        ctk.CTkButton(
            self.frame_inicio,
            text="Registrarse",
            command=self.mostrar_registro,
            width=220,
            height=50,
            font=("Arial", 16),
            corner_radius=10,
            fg_color="#4caf50",
            hover_color="#388e3c"
        ).pack(pady=15)
        
        ctk.CTkButton(
            self.frame_inicio,
            text="Salir",
            command=self.root.quit,
            width=220,
            height=50,
            font=("Arial", 16),
            corner_radius=10,
            fg_color="#f44336",
            hover_color="#d32f2f"
        ).pack(pady=15)
        
        # Frame de login
        self.frame_login = ctk.CTkFrame(self.main_container)
        
        ctk.CTkLabel(
            self.frame_login, 
            text="Iniciar Sesión", 
            font=("Arial", 22, "bold")
        ).pack(pady=(10, 30))
        
        # Campos de entrada
        ctk.CTkLabel(self.frame_login, text="Correo:").pack()
        self.correo_login = ctk.CTkEntry(self.frame_login, width=300, placeholder_text="ejemplo@correo.com")
        self.correo_login.pack(pady=5)
        
        ctk.CTkLabel(self.frame_login, text="Contraseña:").pack(pady=(10, 0))
        self.contrasena_login = ctk.CTkEntry(self.frame_login, width=300, show="*")
        self.contrasena_login.pack(pady=5)
        
        # Botones
        btn_frame = ctk.CTkFrame(self.frame_login, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        ctk.CTkButton(
            btn_frame,
            text="Ingresar",
            command=self.iniciar_sesion,
            width=150,
            height=40,
            font=("Arial", 14),
            corner_radius=8
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            btn_frame,
            text="Regresar",
            command=self.mostrar_pantalla_inicio,
            width=150,
            height=40,
            font=("Arial", 14),
            corner_radius=8,
            fg_color="#6c757d",
            hover_color="#5a6268"
        ).pack(side="left", padx=10)
        
        # Frame de registro
        self.frame_registro = ctk.CTkFrame(self.main_container)
        
        ctk.CTkLabel(
            self.frame_registro, 
            text="Crear Cuenta", 
            font=("Arial", 22, "bold")
        ).pack(pady=(10, 20))
        
        # Campos de registro
        campos = [
            ("Nombre", "nombre_registro"),
            ("Correo", "correo_registro"),
            ("Contraseña", "contrasena_registro", True)
        ]
        
        for campo in campos:
            ctk.CTkLabel(self.frame_registro, text=f"{campo[0]}:").pack()
            if len(campo) == 3:
                entry = ctk.CTkEntry(self.frame_registro, width=350, show="*")
                setattr(self, campo[1], entry)
            else:
                entry = ctk.CTkEntry(self.frame_registro, width=350)
                setattr(self, campo[1], entry)
            entry.pack(pady=5)
        
        # Tipo de usuario
        ctk.CTkLabel(self.frame_registro, text="Tipo de Usuario:").pack(pady=(10, 0))
        self.tipo_usuario = ctk.CTkComboBox(
            self.frame_registro, 
            values=["Cliente", "Administrador"],
            state="readonly",
            width=350
        )
        self.tipo_usuario.set("Cliente")
        self.tipo_usuario.pack(pady=5)
        
        # Botones
        btn_frame = ctk.CTkFrame(self.frame_registro, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        ctk.CTkButton(
            btn_frame,
            text="Registrarse",
            command=self.registrar_usuario,
            width=150,
            height=40,
            font=("Arial", 14),
            corner_radius=8,
            fg_color="#4caf50",
            hover_color="#388e3c"
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            btn_frame,
            text="Regresar",
            command=self.mostrar_pantalla_inicio,
            width=150,
            height=40,
            font=("Arial", 14),
            corner_radius=8,
            fg_color="#6c757d",
            hover_color="#5a6268"
        ).pack(side="left", padx=10)
        
        # Frame del panel principal
        self.frame_panel = ctk.CTkFrame(self.main_container)
        
        # Barra de navegación superior
        self.navbar = ctk.CTkFrame(self.frame_panel, height=50, corner_radius=0)
        self.navbar.pack(fill="x")
        
        # Frame para el contenido principal
        self.main_content = ctk.CTkFrame(self.frame_panel, fg_color="transparent")
        self.main_content.pack(expand=True, fill="both", padx=20, pady=20)

    def mostrar_pantalla_inicio(self):
        self.ocultar_todos_frames()
        self.frame_inicio.pack(expand=True, fill="both")

    def mostrar_login(self):
        self.ocultar_todos_frames()
        self.frame_login.pack(expand=True, fill="both")
        self.correo_login.focus()

    def mostrar_registro(self):
        self.ocultar_todos_frames()
        self.frame_registro.pack(expand=True, fill="both")
        self.nombre_registro.focus()

    def ocultar_todos_frames(self):
        for frame in [self.frame_inicio, self.frame_login, self.frame_registro, self.frame_panel]:
            frame.pack_forget()

    def registrar_usuario(self):
        datos = {
            "nombre": self.nombre_registro.get(),
            "correo": self.correo_registro.get(),
            "contrasena": self.contrasena_registro.get(),
            "tipo": self.tipo_usuario.get()
        }
        
        if not all(datos.values()):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO Usuarios (Nombre, Correo, Contrasena, Tipo) VALUES (?, ?, ?, ?)",
                datos["nombre"], datos["correo"], datos["contrasena"], datos["tipo"]
            )
            self.conn.commit()
            messagebox.showinfo("Éxito", "Usuario registrado correctamente")
            self.mostrar_pantalla_inicio()
        except pyodbc.IntegrityError:
            messagebox.showerror("Error", "El correo ya está registrado")
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar: {str(e)}")

    def iniciar_sesion(self):
        correo = self.correo_login.get()
        contrasena = self.contrasena_login.get()
        
        if not correo or not contrasena:
            messagebox.showerror("Error", "Correo y contraseña son obligatorios")
            return
        
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT UsuarioID, Nombre, Tipo FROM Usuarios WHERE Correo = ? AND Contrasena = ?",
                correo, contrasena
            )
            usuario = cursor.fetchone()
            
            if usuario:
                self.usuario_actual = {
                    "id": usuario.UsuarioID,
                    "nombre": usuario.Nombre,
                    "tipo": usuario.Tipo
                }
                messagebox.showinfo("Bienvenido", f"¡Hola {usuario.Nombre}!")
                self.mostrar_panel_principal()
            else:
                messagebox.showerror("Error", "Credenciales incorrectas")
        except Exception as e:
            messagebox.showerror("Error", f"Error al iniciar sesión: {str(e)}")

    def mostrar_panel_principal(self):
        self.ocultar_todos_frames()
        self.frame_panel.pack(expand=True, fill="both")
        
        # Limpiar navbar y main content
        for widget in self.navbar.winfo_children():
            widget.destroy()
        
        for widget in self.main_content.winfo_children():
            widget.destroy()
        
        # Configurar navbar según tipo de usuario
        if self.usuario_actual["tipo"] == "Administrador":
            botones_admin = [
                ("🎭 Funciones", self.gestionar_funciones),
                ("🏟️ Salas", self.gestionar_salas)
            ]
            for texto, comando in botones_admin:
                ctk.CTkButton(
                    self.navbar,
                    text=texto,
                    command=comando,
                    width=140,
                    height=30,
                    font=("Arial", 12),
                    corner_radius=6
                ).pack(side="left", padx=5)
        
        # Botones comunes
        botones_comunes = [
            ("📅 Cartelera", self.mostrar_cartelera),
            ("🎟️ Mis Reservas", self.mostrar_mis_reservas)
        ]
        for texto, comando in botones_comunes:
            ctk.CTkButton(
                self.navbar,
                text=texto,
                command=comando,
                width=140,
                height=30,
                font=("Arial", 12),
                corner_radius=6
            ).pack(side="left", padx=5)
        
        # Botón de salir
        ctk.CTkButton(
            self.navbar,
            text="🚪 Cerrar Sesión",
            command=self.cerrar_sesion,
            width=140,
            height=30,
            font=("Arial", 12),
            corner_radius=6,
            fg_color="#f44336",
            hover_color="#d32f2f"
        ).pack(side="right", padx=10)
        
        # Mostrar cartelera por defecto
        self.mostrar_cartelera()

    def cerrar_sesion(self):
        self.usuario_actual = None
        self.mostrar_pantalla_inicio()

    def mostrar_cartelera(self):
        # Limpiar contenido principal
        for widget in self.main_content.winfo_children():
            widget.destroy()
        
        # Título
        ctk.CTkLabel(
            self.main_content,
            text="🎥 Cartelera de Eventos",
            font=("Arial", 22, "bold")
        ).pack(pady=10)
        
        # Frame para tabla
        table_frame = ctk.CTkFrame(self.main_content)
        table_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT f.FuncionID, f.NombreEvento, f.Descripcion, f.Duracion, 
                       f.FechaHora, s.Nombre AS Sala, s.Capacidad
                FROM Funciones f
                JOIN Salas s ON f.SalaID = s.SalaID
                WHERE f.FechaHora > GETDATE()
                ORDER BY f.FechaHora
            """)
            funciones = cursor.fetchall()
            
            if not funciones:
                ctk.CTkLabel(self.main_content, text="No hay funciones disponibles").pack()
                return
            
            # Configurar estilo de tabla
            style = ttk.Style()
            style.theme_use("default")
            style.configure("Treeview",
                background="#2a2d2e",
                foreground="white",
                rowheight=25,
                fieldbackground="#343638",
                bordercolor="#343638",
                borderwidth=0)
            style.map("Treeview", background=[("selected", "#22559b")])
            
            style.configure("Treeview.Heading",
                background="#3b8ed0",
                foreground="white",
                relief="flat")
            
            # Crear tabla
            tree = ttk.Treeview(
                table_frame,
                columns=("Nombre", "Descripción", "Duración", "Fecha", "Hora", "Sala"),
                show="headings"
            )
            
            # Configurar columnas
            columnas = [
                ("Nombre", 180),
                ("Descripción", 250),
                ("Duración", 80),
                ("Fecha", 100),
                ("Hora", 80),
                ("Sala", 100)
            ]
            
            for col, width in columnas:
                tree.heading(col, text=col)
                tree.column(col, width=width)
            
            # Scrollbar
            scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side="right", fill="y")
            tree.pack(expand=True, fill="both")
            
            # Llenar tabla
            for funcion in funciones:
                fecha_hora = funcion.FechaHora
                tree.insert("", "end", values=(
                    funcion.NombreEvento,
                    funcion.Descripcion,
                    f"{funcion.Duracion} min",
                    fecha_hora.strftime("%Y-%m-%d"),
                    fecha_hora.strftime("%H:%M"),
                    funcion.Sala
                ), iid=funcion.FuncionID)
            
            # Botón de reserva (solo clientes)
            if self.usuario_actual["tipo"] == "Cliente":
                btn_frame = ctk.CTkFrame(self.main_content)
                btn_frame.pack(pady=10)
                
                ctk.CTkButton(
                    btn_frame,
                    text="🎫 Reservar Boletos",
                    command=lambda: self.reservar_boletos(tree.selection()[0]),
                    width=200,
                    height=40,
                    font=("Arial", 14),
                    corner_radius=8
                ).pack()
        
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la cartelera:\n{str(e)}")

    def reservar_boletos(self, funcion_id):
        self.funcion_seleccionada = funcion_id
        self.asientos_seleccionados = []
        
        try:
            cursor = self.conn.cursor()
            
            # Obtener información de la función
            cursor.execute("""
                SELECT f.NombreEvento, f.FechaHora, s.SalaID, s.Nombre, s.Capacidad
                FROM Funciones f
                JOIN Salas s ON f.SalaID = s.SalaID
                WHERE f.FuncionID = ?
            """, funcion_id)
            funcion = cursor.fetchone()
            
            if not funcion:
                messagebox.showerror("Error", "Función no encontrada")
                return
            
            # Obtener asientos reservados
            cursor.execute("""
                SELECT a.AsientoID, a.Fila, a.Numero
                FROM Reservas r
                JOIN Asientos a ON r.AsientoID = a.AsientoID
                WHERE r.FuncionID = ?
            """, funcion_id)
            asientos_reservados = {(a.Fila, a.Numero): a.AsientoID for a in cursor.fetchall()}
            
            # Obtener todos los asientos
            cursor.execute("""
                SELECT AsientoID, Fila, Numero
                FROM Asientos
                WHERE SalaID = ?
                ORDER BY Fila, Numero
            """, funcion.SalaID)
            todos_asientos = cursor.fetchall()
            
            # Ventana de selección
            seat_window = ctk.CTkToplevel(self.root)
            seat_window.title(f"Selección de Asientos - {funcion.NombreEvento}")
            seat_window.geometry("900x750")  # Tamaño ajustado
            seat_window.resizable(False, False)  # Evitar redimensionamiento
            
            # Frame principal con mejor organización
            main_frame = ctk.CTkFrame(seat_window)
            main_frame.pack(fill='both', expand=True, padx=20, pady=20)
            
            # Frame superior para título
            top_frame = ctk.CTkFrame(main_frame, height=50, fg_color="transparent")
            top_frame.pack(fill='x', pady=(0, 10))
            
            ctk.CTkLabel(
                top_frame,
                text=f"Seleccione asientos para:\n{funcion.NombreEvento}",
                font=("Arial", 18, "bold"),
                justify="center"
            ).pack()
            
            # Frame para la visualización de asientos
            graph_frame = ctk.CTkFrame(main_frame)
            graph_frame.pack(fill='both', expand=True)
            
            # Visualización de asientos mejorada
            fig, ax = plt.subplots(figsize=(10, 6))
            fig.subplots_adjust(left=0.05, right=0.95, bottom=0.1, top=0.9)
            
            # Dibujar pantalla mejorada
            screen = patches.Rectangle((0.1, 0.88), 0.8, 0.06, color='#1a237e', alpha=0.9, ec='gold', lw=2)
            ax.add_patch(screen)
            ax.text(0.5, 0.91, 'P A N T A L L A', 
                    ha='center', va='center', 
                    color='gold', fontsize=12, weight='bold')
            
            # Organizar asientos con mejor distribución
            filas = sorted(set(a.Fila for a in todos_asientos))
            max_num = max(a.Numero for a in todos_asientos)
            
            seat_positions = {}
            seat_size = 0.035  # Tamaño aumentado de los asientos
            vertical_spacing = 0.12  # Espacio entre filas
            
            for i, fila in enumerate(filas):
                asientos_fila = [a for a in todos_asientos if a.Fila == fila]
                for j, asiento in enumerate(asientos_fila):
                    x = 0.15 + (j / (max_num + 1)) * 0.7  # Distribución horizontal mejorada
                    y = 0.75 - (i * vertical_spacing)  # Posición vertical
                    
                    # Color según disponibilidad con mejor contraste
                    if (fila, asiento.Numero) in asientos_reservados:
                        color = '#d32f2f'  # Rojo para ocupado
                        edge_color = '#b71c1c'
                    else:
                        color = '#388e3c'  # Verde para disponible
                        edge_color = '#1b5e20'
                    
                    # Dibujar asiento con borde
                    rect = patches.Rectangle(
                        (x, y), seat_size, seat_size, 
                        color=color, ec=edge_color, lw=1.5
                    )
                    ax.add_patch(rect)
                    
                    # Texto del asiento más legible
                    ax.text(
                        x + seat_size/2, y + seat_size/2, 
                        f"{fila}{asiento.Numero}", 
                        ha='center', va='center', 
                        fontsize=8, color='white', weight='bold'
                    )
                    
                    seat_positions[(x, y)] = (asiento.AsientoID, fila, asiento.Numero, color)
            
            # Configuración final del gráfico
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            ax.set_title('Selección de Asientos', pad=15, fontsize=14, weight='bold')
            
            # Canvas para matplotlib con scroll si es necesario
            canvas = FigureCanvasTkAgg(fig, master=graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
            
            # Frame inferior para controles
            bottom_frame = ctk.CTkFrame(main_frame, height=80)
            bottom_frame.pack(fill='x', pady=(10, 0))
            
            # Etiqueta de selección
            self.selected_seats_label = ctk.CTkLabel(
                bottom_frame,
                text="Asientos seleccionados: Ninguno",
                font=("Arial", 12)
            )
            self.selected_seats_label.pack(pady=(5, 10))
            
            # Frame para botones
            btn_frame = ctk.CTkFrame(bottom_frame, fg_color="transparent")
            btn_frame.pack(pady=(0, 5))
            
            ctk.CTkButton(
                btn_frame,
                text="Confirmar Reserva",
                command=lambda: self.confirmar_reserva(seat_window),
                width=150,
                height=35,
                font=("Arial", 12),
                corner_radius=6,
                fg_color="#4caf50",
                hover_color="#388e3c"
            ).pack(side='left', padx=10)
            
            ctk.CTkButton(
                btn_frame,
                text="Cancelar",
                command=seat_window.destroy,
                width=150,
                height=35,
                font=("Arial", 12),
                corner_radius=6,
                fg_color="#f44336",
                hover_color="#d32f2f"
            ).pack(side='left', padx=10)
            
            # Función para manejar clics - CORREGIDA
            def on_click(event):
                if event.inaxes != ax:
                    return
                
                for (x, y), (asiento_id, fila, numero, color) in seat_positions.items():
                    if (x <= event.xdata <= x + seat_size and y <= event.ydata <= y + seat_size):
                        if color == '#d32f2f':  # Si está ocupado
                            messagebox.showwarning("Ocupado", f"Asiento {fila}{numero} no disponible")
                            return
                        
                        # Cambiar estado de selección
                        if color == '#388e3c':  # Disponible -> Seleccionado
                            seat_positions[(x, y)] = (asiento_id, fila, numero, '#1976d2')  # Azul para seleccionado
                            if asiento_id not in self.asientos_seleccionados:
                                self.asientos_seleccionados.append(asiento_id)
                        elif color == '#1976d2':  # Seleccionado -> Disponible
                            seat_positions[(x, y)] = (asiento_id, fila, numero, '#388e3c')
                            if asiento_id in self.asientos_seleccionados:
                                self.asientos_seleccionados.remove(asiento_id)
                        
                        # Actualizar gráfico
                        for patch in ax.patches[1:]:  # Saltar la pantalla (primer patch)
                            patch.remove()
                        
                        for (x, y), (_, fila, num, col) in seat_positions.items():
                            edge_color = '#0d47a1' if col == '#1976d2' else ('#b71c1c' if col == '#d32f2f' else '#1b5e20')
                            rect = patches.Rectangle(
                                (x, y), seat_size, seat_size, 
                                color=col, ec=edge_color, lw=1.5
                            )
                            ax.add_patch(rect)
                            ax.text(
                                x + seat_size/2, y + seat_size/2, 
                                f"{fila}{num}", 
                                ha='center', va='center', 
                                fontsize=8, color='white', weight='bold'
                            )
                        
                        canvas.draw()
                        update_selected_label()
                        break
            
            # Conectar evento corregido
            canvas.mpl_connect('button_press_event', on_click)
            
            # Función para actualizar etiqueta
            def update_selected_label():
                if self.asientos_seleccionados:
                    cursor.execute("""
                        SELECT Fila, Numero FROM Asientos 
                        WHERE AsientoID IN ({})
                        ORDER BY Fila, Numero
                    """.format(','.join('?' * len(self.asientos_seleccionados))), 
                    self.asientos_seleccionados)
                    
                    seats = cursor.fetchall()
                    seats_str = ", ".join(f"{s.Fila}{s.Numero}" for s in seats)
                    self.selected_seats_label.configure(
                        text=f"Asientos seleccionados: {seats_str}",
                        text_color="#1976d2"
                    )
                else:
                    self.selected_seats_label.configure(
                        text="Asientos seleccionados: Ninguno",
                        text_color="white"
                    )
            
            # Actualización inicial
            update_selected_label()
        
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar los asientos:\n{str(e)}")

    def confirmar_reserva(self, window):
        if not self.asientos_seleccionados:
            messagebox.showwarning("Advertencia", "Seleccione al menos un asiento")
            return
        
        try:
            cursor = self.conn.cursor()
            
            # Verificar disponibilidad
            cursor.execute("""
                SELECT a.AsientoID, a.Fila, a.Numero
                FROM Reservas r
                JOIN Asientos a ON r.AsientoID = a.AsientoID
                WHERE r.FuncionID = ? AND a.AsientoID IN ({})
            """.format(','.join('?' * len(self.asientos_seleccionados))), 
            [self.funcion_seleccionada] + self.asientos_seleccionados)
            
            asientos_ocupados = cursor.fetchall()
            
            if asientos_ocupados:
                ocupados_str = ", ".join(f"{a.Fila}{a.Numero}" for a in asientos_ocupados)
                messagebox.showerror("Error", f"Asientos ya reservados:\n{ocupados_str}")
                return
            
            # Crear reservas
            for asiento_id in self.asientos_seleccionados:
                cursor.execute("""
                    INSERT INTO Reservas (UsuarioID, FuncionID, AsientoID)
                    VALUES (?, ?, ?)
                """, self.usuario_actual["id"], self.funcion_seleccionada, asiento_id)
            
            self.conn.commit()
            messagebox.showinfo("Éxito", "Reserva realizada correctamente")
            window.destroy()
            self.mostrar_mis_reservas()
        
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo completar la reserva:\n{str(e)}")

    def mostrar_mis_reservas(self):
        # Limpiar contenido principal
        for widget in self.main_content.winfo_children():
            widget.destroy()
        
        # Título
        ctk.CTkLabel(
            self.main_content,
            text="🎟️ Mis Reservas",
            font=("Arial", 22, "bold")
        ).pack(pady=10)
        
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT r.ReservaID, f.NombreEvento, f.FechaHora, s.Nombre AS Sala, 
                       a.Fila, a.Numero, r.FechaReserva
                FROM Reservas r
                JOIN Funciones f ON r.FuncionID = f.FuncionID
                JOIN Salas s ON f.SalaID = s.SalaID
                JOIN Asientos a ON r.AsientoID = a.AsientoID
                WHERE r.UsuarioID = ? AND f.FechaHora > GETDATE()
                ORDER BY f.FechaHora
            """, self.usuario_actual["id"])
            reservas = cursor.fetchall()
            
            if not reservas:
                ctk.CTkLabel(self.main_content, text="No tienes reservas activas").pack()
                return
            
            # Frame para tabla
            table_frame = ctk.CTkFrame(self.main_content)
            table_frame.pack(expand=True, fill="both", padx=10, pady=10)
            
            # Configurar estilo de tabla
            style = ttk.Style()
            style.theme_use("default")
            style.configure("Treeview",
                background="#2a2d2e",
                foreground="white",
                rowheight=25,
                fieldbackground="#343638",
                bordercolor="#343638",
                borderwidth=0)
            style.map("Treeview", background=[("selected", "#22559b")])
            
            style.configure("Treeview.Heading",
                background="#3b8ed0",
                foreground="white",
                relief="flat")
            
            # Crear tabla
            tree = ttk.Treeview(
                table_frame,
                columns=("Evento", "Fecha", "Hora", "Sala", "Asiento", "Reservado"),
                show="headings"
            )
            
            # Configurar columnas
            columnas = [
                ("Evento", 180),
                ("Fecha", 100),
                ("Hora", 80),
                ("Sala", 120),
                ("Asiento", 80),
                ("Reservado", 150)
            ]
            
            for col, width in columnas:
                tree.heading(col, text=col)
                tree.column(col, width=width)
            
            # Scrollbar
            scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side="right", fill="y")
            tree.pack(expand=True, fill="both")
            
            # Llenar tabla
            for reserva in reservas:
                fecha_hora = reserva.FechaHora
                tree.insert("", "end", values=(
                    reserva.NombreEvento,
                    fecha_hora.strftime("%Y-%m-%d"),
                    fecha_hora.strftime("%H:%M"),
                    reserva.Sala,
                    f"{reserva.Fila}{reserva.Numero}",
                    reserva.FechaReserva.strftime("%Y-%m-%d %H:%M")
                ), iid=reserva.ReservaID)
            
            # Botón de cancelación
            btn_frame = ctk.CTkFrame(self.main_content)
            btn_frame.pack(pady=10)
            
            ctk.CTkButton(
                btn_frame,
                text="❌ Cancelar Reserva",
                command=lambda: self.cancelar_reserva(tree.selection()[0]),
                width=200,
                height=40,
                font=("Arial", 14),
                corner_radius=8,
                fg_color="#f44336",
                hover_color="#d32f2f"
            ).pack()
        
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las reservas:\n{str(e)}")

    def cancelar_reserva(self, reserva_id):
        if not reserva_id:
            messagebox.showwarning("Advertencia", "Seleccione una reserva")
            return
        
        try:
            cursor = self.conn.cursor()
            
            # Verificar fecha de la función
            cursor.execute("""
                SELECT f.FechaHora 
                FROM Reservas r
                JOIN Funciones f ON r.FuncionID = f.FuncionID
                WHERE r.ReservaID = ?
            """, reserva_id)
            fecha_hora = cursor.fetchone().FechaHora
            
            if fecha_hora < datetime.now():
                messagebox.showerror("Error", "No se puede cancelar una función pasada")
                return
            
            # Eliminar reserva
            cursor.execute("DELETE FROM Reservas WHERE ReservaID = ?", reserva_id)
            self.conn.commit()
            
            messagebox.showinfo("Éxito", "Reserva cancelada")
            self.mostrar_mis_reservas()
        
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cancelar:\n{str(e)}")

    def gestionar_funciones(self):
        # Limpiar contenido principal
        for widget in self.main_content.winfo_children():
            widget.destroy()
        
        # Título
        ctk.CTkLabel(
            self.main_content,
            text="🎭 Gestión de Funciones",
            font=("Arial", 22, "bold")
        ).pack(pady=10)
        
        # Frame para botones
        btn_frame = ctk.CTkFrame(self.main_content)
        btn_frame.pack(pady=10)
        
        # Botones de gestión
        ctk.CTkButton(
            btn_frame,
            text="➕ Agregar Función",
            command=self.agregar_funcion,
            width=160,
            height=35,
            font=("Arial", 12),
            corner_radius=6,
            fg_color="#4caf50",
            hover_color="#388e3c"
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="✏️ Editar Función",
            command=self.editar_funcion,
            width=160,
            height=35,
            font=("Arial", 12),
            corner_radius=6
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="🗑️ Eliminar Función",
            command=self.eliminar_funcion,
            width=160,
            height=35,
            font=("Arial", 12),
            corner_radius=6,
            fg_color="#f44336",
            hover_color="#d32f2f"
        ).pack(side="left", padx=5)
        
        # Frame para tabla
        table_frame = ctk.CTkFrame(self.main_content)
        table_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Configurar estilo de tabla
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
            background="#2a2d2e",
            foreground="white",
            rowheight=25,
            fieldbackground="#343638",
            bordercolor="#343638",
            borderwidth=0)
        style.map("Treeview", background=[("selected", "#22559b")])
        
        style.configure("Treeview.Heading",
            background="#3b8ed0",
            foreground="white",
            relief="flat")
        
        # Crear tabla
        self.funciones_tree = ttk.Treeview(
            table_frame,
            columns=("Nombre", "Descripción", "Duración", "Fecha", "Hora", "Sala"),
            show="headings"
        )
        
        # Configurar columnas
        columnas = [
            ("Nombre", 180),
            ("Descripción", 250),
            ("Duración", 80),
            ("Fecha", 100),
            ("Hora", 80),
            ("Sala", 100)
        ]
        
        for col, width in columnas:
            self.funciones_tree.heading(col, text=col)
            self.funciones_tree.column(col, width=width)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.funciones_tree.yview)
        self.funciones_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.funciones_tree.pack(expand=True, fill="both")
        
        # Cargar funciones
        self.cargar_funciones()

    def cargar_funciones(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT f.FuncionID, f.NombreEvento, f.Descripcion, f.Duracion, 
                       f.FechaHora, s.Nombre AS Sala
                FROM Funciones f
                JOIN Salas s ON f.SalaID = s.SalaID
                ORDER BY f.FechaHora
            """)
            funciones = cursor.fetchall()
            
            # Limpiar tabla
            for item in self.funciones_tree.get_children():
                self.funciones_tree.delete(item)
            
            # Llenar tabla
            for funcion in funciones:
                fecha_hora = funcion.FechaHora
                self.funciones_tree.insert("", "end", values=(
                    funcion.NombreEvento,
                    funcion.Descripcion,
                    f"{funcion.Duracion} min",
                    fecha_hora.strftime("%Y-%m-%d"),
                    fecha_hora.strftime("%H:%M"),
                    funcion.Sala
                ), iid=funcion.FuncionID)
        
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las funciones:\n{str(e)}")

    def agregar_funcion(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT SalaID, Nombre FROM Salas ORDER BY Nombre")
            salas = cursor.fetchall()
            
            if not salas:
                messagebox.showerror("Error", "No hay salas registradas")
                return
            
            # Ventana de agregar función
            add_window = ctk.CTkToplevel(self.root)
            add_window.title("Agregar Función")
            add_window.geometry("500x600")
            add_window.resizable(False, False)
            
            frame = ctk.CTkFrame(add_window)
            frame.pack(expand=True, fill="both", padx=20, pady=20)
            
            ctk.CTkLabel(
                frame,
                text="Nueva Función",
                font=("Arial", 20, "bold")
            ).pack(pady=(10, 20))
            
            # Campos de entrada
            campos = [
                ("Nombre del Evento", "nombre_evento"),
                ("Descripción", "descripcion", "text"),
                ("Duración (minutos)", "duracion"),
                ("Fecha (YYYY-MM-DD)", "fecha"),
                ("Hora (HH:MM)", "hora")
            ]
            
            entries = {}
            for campo in campos:
                ctk.CTkLabel(frame, text=f"{campo[0]}:").pack()
                if len(campo) == 3 and campo[2] == "text":
                    entry = ctk.CTkTextbox(frame, width=400, height=80)
                    entries[campo[1]] = entry
                    entry.pack(pady=5)
                else:
                    entry = ctk.CTkEntry(frame, width=400)
                    entries[campo[1]] = entry
                    entry.pack(pady=5)
            
            # Combobox para salas
            ctk.CTkLabel(frame, text="Sala:").pack(pady=(10, 0))
            sala_var = ctk.StringVar()
            sala_menu = ctk.CTkComboBox(
                frame,
                values=[sala.Nombre for sala in salas],
                variable=sala_var,
                state="readonly",
                width=400
            )
            sala_menu.set(salas[0].Nombre)
            sala_menu.pack(pady=5)
            
            # Función para guardar
            def guardar_funcion():
                datos = {
                    "nombre": entries["nombre_evento"].get(),
                    "descripcion": entries["descripcion"].get("1.0", "end").strip(),
                    "duracion": entries["duracion"].get(),
                    "fecha": entries["fecha"].get(),
                    "hora": entries["hora"].get(),
                    "sala": sala_var.get()
                }
                
                if not all(datos.values()):
                    messagebox.showerror("Error", "Todos los campos son obligatorios")
                    return
                
                try:
                    # Validar duración
                    duracion = int(datos["duracion"])
                    if duracion <= 0:
                        raise ValueError("La duración debe ser positiva")
                    
                    # Validar fecha y hora
                    fecha_hora = datetime.strptime(f"{datos['fecha']} {datos['hora']}", "%Y-%m-%d %H:%M")
                    if fecha_hora < datetime.now():
                        raise ValueError("La fecha debe ser futura")
                    
                    # Obtener ID de sala
                    sala_id = next(sala.SalaID for sala in salas if sala.Nombre == datos["sala"])
                    
                    # Insertar función
                    cursor.execute("""
                        INSERT INTO Funciones (NombreEvento, Descripcion, Duracion, FechaHora, SalaID)
                        VALUES (?, ?, ?, ?, ?)
                    """, datos["nombre"], datos["descripcion"], duracion, fecha_hora, sala_id)
                    
                    self.conn.commit()
                    messagebox.showinfo("Éxito", "Función agregada correctamente")
                    add_window.destroy()
                    self.cargar_funciones()
                
                except ValueError as ve:
                    messagebox.showerror("Error", f"Datos inválidos:\n{str(ve)}")
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo agregar la función:\n{str(e)}")
            
            # Botón de guardar
            ctk.CTkButton(
                frame,
                text="Guardar Función",
                command=guardar_funcion,
                width=200,
                height=40,
                font=("Arial", 14),
                corner_radius=8,
                fg_color="#4caf50",
                hover_color="#388e3c"
            ).pack(pady=20)
        
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la información:\n{str(e)}")

    def editar_funcion(self):
        seleccion = self.funciones_tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una función")
            return
        
        funcion_id = seleccion[0]
        
        try:
            cursor = self.conn.cursor()
            
            # Obtener información actual
            cursor.execute("""
                SELECT f.NombreEvento, f.Descripcion, f.Duracion, f.FechaHora, s.SalaID, s.Nombre
                FROM Funciones f
                JOIN Salas s ON f.SalaID = s.SalaID
                WHERE f.FuncionID = ?
            """, funcion_id)
            funcion = cursor.fetchone()
            
            if not funcion:
                messagebox.showerror("Error", "Función no encontrada")
                return
            
            # Obtener salas disponibles
            cursor.execute("SELECT SalaID, Nombre FROM Salas ORDER BY Nombre")
            salas = cursor.fetchall()
            
            # Ventana de edición
            edit_window = ctk.CTkToplevel(self.root)
            edit_window.title("Editar Función")
            edit_window.geometry("500x600")
            edit_window.resizable(False, False)
            
            frame = ctk.CTkFrame(edit_window)
            frame.pack(expand=True, fill="both", padx=20, pady=20)
            
            ctk.CTkLabel(
                frame,
                text="Editar Función",
                font=("Arial", 20, "bold")
            ).pack(pady=(10, 20))
            
            # Campos de entrada con valores actuales
            fecha_hora = funcion.FechaHora
            
            ctk.CTkLabel(frame, text="Nombre del Evento:").pack()
            nombre_entry = ctk.CTkEntry(frame, width=400)
            nombre_entry.insert(0, funcion.NombreEvento)
            nombre_entry.pack(pady=5)
            
            ctk.CTkLabel(frame, text="Descripción:").pack()
            desc_entry = ctk.CTkTextbox(frame, width=400, height=80)
            desc_entry.insert("1.0", funcion.Descripcion)
            desc_entry.pack(pady=5)
            
            ctk.CTkLabel(frame, text="Duración (minutos):").pack()
            duracion_entry = ctk.CTkEntry(frame, width=400)
            duracion_entry.insert(0, str(funcion.Duracion))
            duracion_entry.pack(pady=5)
            
            ctk.CTkLabel(frame, text="Fecha (YYYY-MM-DD):").pack()
            fecha_entry = ctk.CTkEntry(frame, width=400)
            fecha_entry.insert(0, fecha_hora.strftime("%Y-%m-%d"))
            fecha_entry.pack(pady=5)
            
            ctk.CTkLabel(frame, text="Hora (HH:MM):").pack()
            hora_entry = ctk.CTkEntry(frame, width=400)
            hora_entry.insert(0, fecha_hora.strftime("%H:%M"))
            hora_entry.pack(pady=5)
            
            # Combobox para salas
            ctk.CTkLabel(frame, text="Sala:").pack(pady=(10, 0))
            sala_var = ctk.StringVar()
            sala_menu = ctk.CTkComboBox(
                frame,
                values=[sala.Nombre for sala in salas],
                variable=sala_var,
                state="readonly",
                width=400
            )
            sala_menu.set(funcion.Nombre)
            sala_menu.pack(pady=5)
            
            # Función para actualizar
            def actualizar_funcion():
                datos = {
                    "nombre": nombre_entry.get(),
                    "descripcion": desc_entry.get("1.0", "end").strip(),
                    "duracion": duracion_entry.get(),
                    "fecha": fecha_entry.get(),
                    "hora": hora_entry.get(),
                    "sala": sala_var.get()
                }
                
                if not all(datos.values()):
                    messagebox.showerror("Error", "Todos los campos son obligatorios")
                    return
                
                try:
                    # Validar duración
                    duracion = int(datos["duracion"])
                    if duracion <= 0:
                        raise ValueError("La duración debe ser positiva")
                    
                    # Validar fecha y hora
                    nueva_fecha_hora = datetime.strptime(f"{datos['fecha']} {datos['hora']}", "%Y-%m-%d %H:%M")
                    
                    # Obtener ID de sala
                    sala_id = next(sala.SalaID for sala in salas if sala.Nombre == datos["sala"])
                    
                    # Verificar si hay reservas
                    cursor.execute("SELECT COUNT(*) FROM Reservas WHERE FuncionID = ?", funcion_id)
                    num_reservas = cursor.fetchone()[0]
                    
                    if num_reservas > 0 and (funcion.SalaID != sala_id or funcion.FechaHora != nueva_fecha_hora):
                        if not messagebox.askyesno("Confirmar", "Esta función tiene reservas. ¿Continuar?"):
                            return
                    
                    # Actualizar función
                    cursor.execute("""
                        UPDATE Funciones 
                        SET NombreEvento = ?, Descripcion = ?, Duracion = ?, 
                            FechaHora = ?, SalaID = ?
                        WHERE FuncionID = ?
                    """, datos["nombre"], datos["descripcion"], duracion, nueva_fecha_hora, sala_id, funcion_id)
                    
                    self.conn.commit()
                    messagebox.showinfo("Éxito", "Función actualizada")
                    edit_window.destroy()
                    self.cargar_funciones()
                
                except ValueError as ve:
                    messagebox.showerror("Error", f"Datos inválidos:\n{str(ve)}")
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo actualizar:\n{str(e)}")
            
            # Botón de guardar
            ctk.CTkButton(
                frame,
                text="Guardar Cambios",
                command=actualizar_funcion,
                width=200,
                height=40,
                font=("Arial", 14),
                corner_radius=8,
                fg_color="#4caf50",
                hover_color="#388e3c"
            ).pack(pady=20)
        
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la función:\n{str(e)}")

    def eliminar_funcion(self):
        seleccion = self.funciones_tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una función")
            return
        
        funcion_id = seleccion[0]
        
        try:
            cursor = self.conn.cursor()
            
            # Verificar reservas
            cursor.execute("SELECT COUNT(*) FROM Reservas WHERE FuncionID = ?", funcion_id)
            num_reservas = cursor.fetchone()[0]
            
            if num_reservas > 0:
                if not messagebox.askyesno("Confirmar", f"Esta función tiene {num_reservas} reserva(s). ¿Eliminar?"):
                    return
                
                # Eliminar reservas primero
                cursor.execute("DELETE FROM Reservas WHERE FuncionID = ?", funcion_id)
            
            # Eliminar función
            cursor.execute("DELETE FROM Funciones WHERE FuncionID = ?", funcion_id)
            self.conn.commit()
            
            messagebox.showinfo("Éxito", "Función eliminada")
            self.cargar_funciones()
        
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar:\n{str(e)}")

    def gestionar_salas(self):
        # Limpiar contenido principal
        for widget in self.main_content.winfo_children():
            widget.destroy()
        
        # Título
        ctk.CTkLabel(
            self.main_content,
            text="🏟️ Gestión de Salas",
            font=("Arial", 22, "bold")
        ).pack(pady=10)
        
        # Frame para botones
        btn_frame = ctk.CTkFrame(self.main_content)
        btn_frame.pack(pady=10)
        
        # Botones de gestión
        ctk.CTkButton(
            btn_frame,
            text="➕ Agregar Sala",
            command=self.agregar_sala,
            width=160,
            height=35,
            font=("Arial", 12),
            corner_radius=6,
            fg_color="#4caf50",
            hover_color="#388e3c"
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="✏️ Editar Sala",
            command=self.editar_sala,
            width=160,
            height=35,
            font=("Arial", 12),
            corner_radius=6
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="🗑️ Eliminar Sala",
            command=self.eliminar_sala,
            width=160,
            height=35,
            font=("Arial", 12),
            corner_radius=6,
            fg_color="#f44336",
            hover_color="#d32f2f"
        ).pack(side="left", padx=5)
        
        # Frame para tabla
        table_frame = ctk.CTkFrame(self.main_content)
        table_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Configurar estilo de tabla
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
            background="#2a2d2e",
            foreground="white",
            rowheight=25,
            fieldbackground="#343638",
            bordercolor="#343638",
            borderwidth=0)
        style.map("Treeview", background=[("selected", "#22559b")])
        
        style.configure("Treeview.Heading",
            background="#3b8ed0",
            foreground="white",
            relief="flat")
        
        # Crear tabla
        self.salas_tree = ttk.Treeview(
            table_frame,
            columns=("Nombre", "Capacidad"),
            show="headings"
        )
        
        # Configurar columnas
        columnas = [
            ("Nombre", 250),
            ("Capacidad", 150)
        ]
        
        for col, width in columnas:
            self.salas_tree.heading(col, text=col)
            self.salas_tree.column(col, width=width)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.salas_tree.yview)
        self.salas_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.salas_tree.pack(expand=True, fill="both")
        
        # Cargar salas
        self.cargar_salas()

    def cargar_salas(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT SalaID, Nombre, Capacidad FROM Salas ORDER BY Nombre")
            salas = cursor.fetchall()
            
            # Limpiar tabla
            for item in self.salas_tree.get_children():
                self.salas_tree.delete(item)
            
            # Llenar tabla
            for sala in salas:
                self.salas_tree.insert("", "end", values=(
                    sala.Nombre,
                    sala.Capacidad
                ), iid=sala.SalaID)
        
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las salas:\n{str(e)}")

    def agregar_sala(self):
        # Ventana de agregar sala
        add_window = ctk.CTkToplevel(self.root)
        add_window.title("Agregar Sala")
        add_window.geometry("400x300")
        add_window.resizable(False, False)
        
        frame = ctk.CTkFrame(add_window)
        frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        ctk.CTkLabel(
            frame,
            text="Nueva Sala",
            font=("Arial", 20, "bold")
        ).pack(pady=(10, 20))
        
        # Campos de entrada
        ctk.CTkLabel(frame, text="Nombre:").pack()
        nombre_entry = ctk.CTkEntry(frame, width=300)
        nombre_entry.pack(pady=5)
        
        ctk.CTkLabel(frame, text="Capacidad:").pack(pady=(10, 0))
        capacidad_entry = ctk.CTkEntry(frame, width=300)
        capacidad_entry.pack(pady=5)
        
        # Función para guardar - VERSIÓN CORREGIDA
        def guardar_sala():
            nombre = nombre_entry.get()
            capacidad = capacidad_entry.get()
            
            if not nombre or not capacidad:
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
            
            try:
                capacidad = int(capacidad)
                if capacidad <= 0:
                    raise ValueError("La capacidad debe ser positiva")
                
                cursor = self.conn.cursor()
                
                # SOLUCIÓN 1: Usar OUTPUT INSERTED para obtener el ID en una sola operación
                cursor.execute(
                    "INSERT INTO Salas (Nombre, Capacidad) OUTPUT INSERTED.SalaID VALUES (?, ?)", 
                    (nombre, capacidad)  # Nota: parámetros como tupla
                )
                
                # Obtener el ID de la sala recién creada
                result = cursor.fetchone()
                if not result:
                    raise ValueError("No se pudo obtener el ID de la sala creada")
                
                sala_id = result.SalaID
                
                # SOLUCIÓN 2: Crear transacción explícita
                try:
                    # Crear asientos automáticamente
                    num_filas = (capacidad + 9) // 10
                    letras_filas = string.ascii_uppercase[:num_filas]
                    
                    for i, letra in enumerate(letras_filas):
                        asientos_en_fila = 10 if (i < num_filas - 1) else (capacidad % 10 or 10)
                        
                        for numero in range(1, asientos_en_fila + 1):
                            # SOLUCIÓN 3: Verificar sala_id antes de insertar
                            if not sala_id:
                                raise ValueError("ID de sala no válido")
                            
                            cursor.execute(
                                "INSERT INTO Asientos (SalaID, Fila, Numero) VALUES (?, ?, ?)",
                                (sala_id, letra, numero)  # Parámetros como tupla
                            )
                    
                    self.conn.commit()
                    messagebox.showinfo("Éxito", f"Sala '{nombre}' creada con {capacidad} asientos")
                    add_window.destroy()
                    self.cargar_salas()
                    
                except Exception as e:
                    self.conn.rollback()
                    raise e
                    
            except ValueError as ve:
                self.conn.rollback()
                messagebox.showerror("Error", f"Dato inválido:\n{str(ve)}")
            except Exception as e:
                self.conn.rollback()
                messagebox.showerror("Error", f"No se pudo agregar:\n{str(e)}")
        
        # Botón de guardar
        ctk.CTkButton(
            frame,
            text="Guardar Sala",
            command=guardar_sala,
            width=200,
            height=40,
            font=("Arial", 14),
            corner_radius=8,
            fg_color="#4caf50",
            hover_color="#388e3c"
        ).pack(pady=20)

    def editar_sala(self):
        seleccion = self.salas_tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una sala")
            return
        
        sala_id = seleccion[0]
        
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT Nombre, Capacidad FROM Salas WHERE SalaID = ?",
                sala_id
            )
            sala = cursor.fetchone()
            
            if not sala:
                messagebox.showerror("Error", "Sala no encontrada")
                return
            
            # Ventana de edición
            edit_window = ctk.CTkToplevel(self.root)
            edit_window.title("Editar Sala")
            edit_window.geometry("400x300")
            edit_window.resizable(False, False)
            
            frame = ctk.CTkFrame(edit_window)
            frame.pack(expand=True, fill="both", padx=20, pady=20)
            
            ctk.CTkLabel(
                frame,
                text="Editar Sala",
                font=("Arial", 20, "bold")
            ).pack(pady=(10, 20))
            
            # Campos de entrada con valores actuales
            ctk.CTkLabel(frame, text="Nombre:").pack()
            nombre_entry = ctk.CTkEntry(frame, width=300)
            nombre_entry.insert(0, sala.Nombre)
            nombre_entry.pack(pady=5)
            
            ctk.CTkLabel(frame, text="Capacidad:").pack(pady=(10, 0))
            capacidad_entry = ctk.CTkEntry(frame, width=300)
            capacidad_entry.insert(0, str(sala.Capacidad))
            capacidad_entry.pack(pady=5)
            
            # Función para actualizar
            def actualizar_sala():
                nombre = nombre_entry.get()
                capacidad = capacidad_entry.get()
                
                if not nombre or not capacidad:
                    messagebox.showerror("Error", "Todos los campos son obligatorios")
                    return
                
                try:
                    capacidad = int(capacidad)
                    if capacidad <= 0:
                        raise ValueError("La capacidad debe ser positiva")
                    
                    # Verificar funciones programadas
                    cursor.execute("SELECT COUNT(*) FROM Funciones WHERE SalaID = ?", sala_id)
                    num_funciones = cursor.fetchone()[0]
                    
                    if num_funciones > 0:
                        messagebox.showerror("Error", "No se puede modificar una sala con funciones programadas")
                        return
                    
                    # Actualizar sala
                    cursor.execute(
                        "UPDATE Salas SET Nombre = ?, Capacidad = ? WHERE SalaID = ?",
                        nombre, capacidad, sala_id
                    )
                    
                    # Eliminar asientos existentes y crear nuevos
                    cursor.execute("DELETE FROM Asientos WHERE SalaID = ?", sala_id)
                    
                    # Crear asientos automáticamente (10 asientos por fila)
                    num_filas = (capacidad + 9) // 10  # Redondeo hacia arriba
                    letras_filas = string.ascii_uppercase[:num_filas]
                    
                    for i, letra in enumerate(letras_filas):
                        # Calcular cuántos asientos en esta fila (10 o el resto)
                        asientos_en_fila = 10 if (i < num_filas - 1) else (capacidad % 10 or 10)
                        
                        for numero in range(1, asientos_en_fila + 1):
                            cursor.execute(
                                "INSERT INTO Asientos (SalaID, Fila, Numero) VALUES (?, ?, ?)",
                                sala_id, letra, numero
                            )
                    
                    self.conn.commit()
                    messagebox.showinfo("Éxito", "Sala actualizada")
                    edit_window.destroy()
                    self.cargar_salas()
                
                except ValueError as ve:
                    messagebox.showerror("Error", f"Dato inválido:\n{str(ve)}")
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo actualizar:\n{str(e)}")
            
            # Botón de guardar
            ctk.CTkButton(
                frame,
                text="Guardar Cambios",
                command=actualizar_sala,
                width=200,
                height=40,
                font=("Arial", 14),
                corner_radius=8,
                fg_color="#4caf50",
                hover_color="#388e3c"
            ).pack(pady=20)
        
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la sala:\n{str(e)}")

    def eliminar_sala(self):
        seleccion = self.salas_tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una sala")
            return
        
        sala_id = seleccion[0]
        
        try:
            cursor = self.conn.cursor()
            
            # Verificar funciones programadas
            cursor.execute("SELECT COUNT(*) FROM Funciones WHERE SalaID = ?", sala_id)
            num_funciones = cursor.fetchone()[0]
            
            if num_funciones > 0:
                messagebox.showerror("Error", "No se puede eliminar una sala con funciones programadas")
                return
            
            # Eliminar asientos primero
            cursor.execute("DELETE FROM Asientos WHERE SalaID = ?", sala_id)
            
            # Eliminar sala
            cursor.execute("DELETE FROM Salas WHERE SalaID = ?", sala_id)
            self.conn.commit()
            
            messagebox.showinfo("Éxito", "Sala eliminada")
            self.cargar_salas()
        
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar:\n{str(e)}")

if __name__ == "__main__":
    root = ctk.CTk()
    app = SistemaBoletos(root)
    root.mainloop()