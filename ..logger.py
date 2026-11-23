"""
Módulo encargado de registrar eventos y errores en un archivo de texto plano (.log).
"""
from datetime import datetime


class RegistradorLogs:
    """Clase utilitaria para gestionar la escritura segura de logs en disco."""

    def __init__(self, ruta_archivo: str = "sistema_fj.log"):
        # Define la ruta del archivo donde se almacenarán los registros
        self.ruta_archivo = ruta_archivo

    def registrar_evento(self, nivel: str, mensaje: str) -> None:
        """
        Escribe una línea de registro con marca de tiempo en el archivo de logs.
        Usa bloques try/except/finally para evitar que un fallo de escritura detenga el sistema.
        """
        # Obtiene la fecha y hora actual en formato legible
        marca_tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Formatea la línea de texto a guardar
        linea = f"[{marca_tiempo}] [{nivel.upper()}] {mensaje}\n"
        archivo = None

        try:
            # Abre el archivo en modo 'append' (añadir al final) con codificación UTF-8
            archivo = open(self.ruta_archivo, mode="a", encoding="utf-8")
            # Escribe la línea formateada en el archivo
            archivo.write(linea)
        except OSError as error_io:
            # Si ocurre un error de disco o permisos, lo muestra en consola sin colapsar
            print(f"ADVERTENCIA CRÍTICA: No se pudo escribir en el archivo de log: {error_io}")
        finally:
            # Garantiza que el archivo se cierre correctamente si llegó a abrirse
            if archivo is not None and not archivo.closed:
                archivo.close()

    def registrar_error(self, mensaje: str, excepcion: Exception) -> None:
        """
        Registra un error detallado junto con su excepción original o encadenada.
        """
        # Construye el detalle técnico incluyendo el tipo de excepción y su mensaje
        detalle_error = f"{mensaje} | Tipo: {type(excepcion).__name__} | Detalle: {excepcion}"
        # Si existe una excepción encadenada (__cause__), también la registra
        if excepcion.__cause__ is not None:
            detalle_error += f" | Causa original: {type(excepcion.__cause__).__name__}: {excepcion.__cause__}"
        
        # Llama al método de escritura con nivel ERROR
        self.registrar_evento("ERROR", detalle_error)
