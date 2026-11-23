"""
Módulo base que define la clase abstracta Entidad y la clase Cliente
con encapsulación estricta y validaciones robustas.
"""
from abc import ABC, abstractmethod
import re
from src.excepciones import DatoInvalidoError, ParametroFaltanteError


class Entidad(ABC):
    """Clase abstracta que representa cualquier entidad general del sistema Software FJ."""

    def __init__(self, id_entidad: str):
        # Valida que el identificador no sea nulo ni una cadena vacía
        if not id_entidad or not str(id_entidad).strip():
            raise ParametroFaltanteError("El identificador de la entidad es obligatorio.")
        # Almacena el identificador como atributo protegido
        self._id = str(id_entidad).strip()

    @property
    def id(self) -> str:
        """Retorna el identificador único de la entidad (solo lectura)."""
        return self._id

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Método abstracto que obliga a las clases hijas a describir su información."""
        pass


class Cliente(Entidad):
    """
    Representa un cliente de Software FJ.
    Aplica encapsulación mediante atributos privados y propiedades (@property) con validación.
    """

    def __init__(self, id_cliente: str, nombre: str, correo: str, telefono: str):
        # Inicializa la clase padre Entidad validando el ID
        super().__init__(id_cliente)
        # Asigna los atributos usando los setters para garantizar todas las validaciones
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self) -> str:
        """Obtiene el nombre completo del cliente."""
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        """Valida y asigna el nombre del cliente."""
        if not valor or not str(valor).strip():
            raise ParametroFaltanteError("El nombre del cliente no puede estar vacío.")
        if len(str(valor).strip()) < 3:
            raise DatoInvalidoError("El nombre del cliente debe tener al menos 3 caracteres.")
        self.__nombre = str(valor).strip()

    @property
    def correo(self) -> str:
        """Obtiene el correo electrónico del cliente."""
        return self.__correo

    @correo.setter
    def correo(self, valor: str) -> None:
        """Valida el formato básico de correo electrónico antes de asignarlo."""
        if not valor or not str(valor).strip():
            raise ParametroFaltanteError("El correo electrónico es obligatorio.")
        patron_correo = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(patron_correo, str(valor).strip()):
            raise DatoInvalidoError(f"El correo '{valor}' no tiene un formato válido.")
        self.__correo = str(valor).strip().lower()

    @property
    def telefono(self) -> str:
        """Obtiene el número de teléfono del cliente."""
        return self.__telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        """Valida que el teléfono contenga entre 7 y 15 dígitos numéricos."""
        if not valor or not str(valor).strip():
            raise ParametroFaltanteError("El teléfono del cliente es obligatorio.")
        limpio = str(valor).strip()
        if not limpio.isdigit() or not (7 <= len(limpio) <= 15):
            raise DatoInvalidoError(f"El teléfono '{valor}' debe contener entre 7 y 15 dígitos.")
        self.__telefono = limpio

    def obtener_resumen(self) -> str:
        """Implementación del método abstracto para mostrar los datos del cliente."""
        return f"Cliente [{self.id}]: {self.nombre} | Correo: {self.correo} | Tel: {self.telefono}"
