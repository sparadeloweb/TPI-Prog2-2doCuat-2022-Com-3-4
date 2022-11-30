import sqlite3
from rich import print
from rich.prompt import Prompt
from rich.console import Console
from rich.table import Table
from rich.prompt import Confirm

class ProgramaPrincipal:
    def menu(self):
        while True:
            print("[bold]Concesionaria[/bold] [bold green italic]Paradelo&Gambino[/bold green italic]")
            print("[white bold]5 - Listado de Automoviles[/white bold]")
            print("[white bold]4 - Cargar Disponibilidad[/white bold]")
            print("[white bold]3 - Eliminar Automovil[/white bold]")
            print("[white bold]2 - Modificar Automovil[/white bold]")
            print("[white bold]1 - Cargar Automovil[/white bold]")
            print("[white bold]0 - Salir de menu[/white bold]")
            nro = int(Prompt.ask("[white bold]Por favor ingrese un número[/white bold]"))
            if nro == 1:
                marca = Prompt.ask("[white bold]Por favor ingrese la marca del automovil[/white bold]")
                modelo = Prompt.ask("[white bold]Por favor ingrese el modelo del automovil[/white bold]")
                precio = Prompt.ask("[white bold]Por favor ingrese el precio del automovil[/white bold]")
                cantidadDisponibles = Prompt.ask("[white bold]Por favor ingrese la cantidad de unidades disponibles[/white bold]")
                nuevo_automovil = Automovil(marca, modelo , precio, cantidadDisponibles)
                nuevo_automovil.cargar_automovil()
            if nro == 2:
                marca = Prompt.ask("[white bold]Por favor ingrese el nombre de la marca[/white bold]")
                modelo = Prompt.ask("[white bold]Por favor ingrese el nombre del modelo[/white bold]")
                precio = Prompt.ask("[white bold]Por favor ingrese el nuevo precio[/white bold]")
                automovil_a_modificar = Automovil(marca, modelo, precio)
                automovil_a_modificar.modificar_automovil()
            if nro == 3:
                marca = Prompt.ask("[white bold]Por favor ingrese el nombre de la marca[/white bold]")
                modelo = Prompt.ask("[white bold]Por favor ingrese el nombre del modelo[/white bold]")
                automovil_a_borrar = Automovil(marca, modelo)
                confirm = Prompt.ask("[white bold]Estas seguro de que deseas elimintar este automovil?[/white bold] [green bold](S/N)[/green bold]")
                if confirm == 'S' or confirm == 's' or confirm == 'N' or confirm == 'n':
                    if confirm == 'S' or 's':
                        automovil_a_borrar.eliminar_automovil()
                    else:
                        return 0
                else:
                    print('[red bold]Opción inválida 🔴[/red bold]')
            if nro == 4:
                marca = Prompt.ask("[white bold]Por favor ingrese el nombre de la marca[/white bold]")
                modelo = Prompt.ask("[white bold]Por favor ingrese el nombre del modelo[/white bold]")
                restar_o_sumar = Prompt.ask("[white bold]Desea restar o sumar?[/white bold] [green bold](restar/sumar)[/green bold]")
                if restar_o_sumar == 'restar' or restar_o_sumar == 'Restar' or restar_o_sumar == 'sumar' or restar_o_sumar == 'Sumar':
                    if restar_o_sumar == 'Sumar' or restar_o_sumar == 'sumar':
                        cantidad_a_sumar = Prompt.ask("[white bold]Por favor ingrese la cantidad a sumar[/white bold]")
                        automovil_a_modificar = Automovil(marca, modelo, modifyQuantityValue = cantidad_a_sumar, restar_o_sumar = "+")
                        automovil_a_modificar.modificar_disponibilidad()
                    elif restar_o_sumar == 'restar' or restar_o_sumar == 'Restar':
                        cantidad_a_restar = Prompt.ask("[white bold]Por favor ingrese la cantidad a restar[/white bold]")
                        automovil_a_modificar = Automovil(marca, modelo, modifyQuantityValue = cantidad_a_restar, restar_o_sumar = "-")
                        automovil_a_modificar.modificar_disponibilidad()
                    else:
                        print('[red bold]Opción inválida 🔴[/red bold]')
            if nro == 5:
                Automovil.obtener_automoviles()
            if nro == 0:
                break
    
    def crearTablas(self):
        conexion = Conexiones()
        conexion.abrirConexion()
        conexion.miCursor.execute("CREATE TABLE IF NOT EXISTS AUTOMOVILES (id_automovil INTEGER PRIMARY KEY , marca  VARCHAR(30) ,modelo  VARCHAR(30),precio FLOAT NOT NULL, cantidadDisponibles INTEGER NOT NULL,UNIQUE(marca,modelo))")    
        conexion.miConexion.commit()       
        conexion.cerrarConexion()

class Automovil:
    def __init__(self, marca, modelo, precio = None, cantidadDisponibles = None, modifyQuantityValue = 0, restar_o_sumar = None):
        self.marca = marca
        self.modelo = modelo
        self.precio = precio
        self.modifyQuantityValue = modifyQuantityValue
        self.restar_o_sumar = restar_o_sumar
        self.cantidadDisponibles = cantidadDisponibles
        
    def cargar_automovil(self):
        conexion = Conexiones()
        conexion.abrirConexion()
        try:
            conexion.miCursor.execute("INSERT INTO AUTOMOVILES(marca,modelo,precio,cantidadDisponibles) VALUES('{}', '{}','{}','{}')".format(self.marca, self.modelo,self.precio,self.cantidadDisponibles))
            conexion.miConexion.commit()
            print("[green bold]Automovil cargado exitosamente 🟢[/green bold]")
        except:
            print("[red bold]Error al agregar un automovil 🔴[/red bold]")
        finally:
            conexion.cerrarConexion()
    
    
    def modificar_automovil(self):
        conexion = Conexiones()
        conexion.abrirConexion()
        try:
            conexion.miCursor.execute("UPDATE AUTOMOVILES SET precio='{}' where marca='{}' and modelo='{}' ".format(self.precio,self.marca,self.modelo))
            conexion.miConexion.commit()
            if conexion.miCursor.rowcount > 0:
                print("[green bold]Automovil modificado correctamente 🟢[/green bold]")
            else:
                print('[red bold]No se encontró el automovil 🔴[/red bold]')
        except:
            print('[red bold]Error al actualizar un automovil 🔴[/red bold]')
        finally:
            conexion.cerrarConexion()
    
    def modificar_disponibilidad(self):
        conexion = Conexiones()
        conexion.abrirConexion()
        try:
            conexion.miCursor.execute(f"UPDATE AUTOMOVILES SET cantidadDisponibles = cantidadDisponibles {self.restar_o_sumar} {self.modifyQuantityValue} where marca='{self.marca}' and modelo='{self.modelo}'")
            conexion.miConexion.commit()
            if conexion.miCursor.rowcount > 0:
                print("[green bold]Automovil modificado correctamente 🟢[/green bold]")
            else:
                print('[red bold]No se encontró el automovil 🔴[/red bold]')
        except:
            print('[red bold]Error al actualizar un automovil 🔴[/red bold]', sys.exc_info()[0])
        finally:
            conexion.cerrarConexion()
    
    def eliminar_automovil(self):
        conexion = Conexiones()
        conexion.abrirConexion()
        try:
            conexion.miCursor.execute("DELETE FROM AUTOMOVILES WHERE marca='{}' and modelo='{}'".format(self.marca,self.modelo))
            conexion.miConexion.commit()
            if conexion.miCursor.rowcount > 0:
                print("[green bold]Automovil eliminado correctamente 🟢[/green bold]")
            else:
                print('[red bold]No se encontró el automovil 🔴[/red bold]')
            
        except:
            print('[red bold]Error al actualizar un automovil 🔴[/red bold]')
        finally:
            conexion.cerrarConexion()
    
    @classmethod
    def obtener_automoviles(cls):
        conexion = Conexiones()
        conexion.abrirConexion()
        console = Console()
        table = Table()
        try:
            conexion.miCursor.execute("SELECT * FROM AUTOMOVILES")
            rows = conexion.miCursor.fetchall()

            if len(rows) > 0:
                column_helper = 0
                for row in rows:
                    if column_helper == 0:
                        column_array = dict(row).keys()
                        for column in column_array:
                            table.add_column(column)
                        column_helper = 1

                    row_values = list(row)

                    for i, value in enumerate(row_values):
                        row_values[i] = str(row_values[i])

                    table.add_row(*row_values)
                
                console.print(table)

                print("[green bold]Listado de automoviles obtenido correctamente 🟢[/green bold]")

            else:
                print('[red bold]No hay automoviles cargados 🔴[/red bold]')
        except:
            print('[red bold]Error al obtener listado de automoviles 🔴[/red bold]')
        finally:
            conexion.cerrarConexion()
        
    
class Conexiones:
    
    def abrirConexion(self):
        self.miConexion = sqlite3.connect("concesionaria.db")
        self.miConexion.row_factory = sqlite3.Row
        self.miCursor = self.miConexion.cursor()
        
    def cerrarConexion(self):
        self.miConexion.close()   


            
programa = ProgramaPrincipal()
programa.crearTablas()
programa.menu()