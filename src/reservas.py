"""
Módulo que implementa la clase Reserva y el gestor central del sistema Software FJ.
Controla estados, validación de disponibilidad, cálculo de totales, encadenamiento de
excepciones y registro automático en el archivo de logs.
"""
from datetime import datetime
from typing import List
from src.entidades import Cliente
from src.servicios import Servicio
from src.logger import RegistradorLogs
from src.excepciones import (
    DatoInvalidoError,
    ParametroFaltanteError,
    OperacionNoPermitidaError,
    ReservaError,
    ErrorSistemaFJ,
)


class Reserva:
    """Representa una reserva que vincula un Cliente con un Servicio en una fecha dada."""

    ESTADOS_VALIDOS = ("PENDIENTE", "CONFIRMADA", "CANCELADA")

    def __init__(
        self,
        id_reserva: str,
        cliente: Cliente,
        servicio: Servicio,
        fecha: str,
        cantidad: int,
        descuento: float = 0.0,
    ):
        if not id_reserva or not str(id_reserva).strip():
            raise ParametroFaltanteError("El ID de la reserva es obligatorio.")
        if not isinstance(cliente, Cliente):
            raise DatoInvalidoError("Se requiere una instancia válida de Cliente.")
        if not isinstance(servicio, Servicio):
            raise DatoInvalidoError("Se requiere una instancia válida de Servicio.")

        # Valida formato de fecha YYYY-MM-DD
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError as err_fecha:
            raise DatoInvalidoError(f"La fecha '{fecha}' no cumple el formato YYYY-MM-DD.") from err_fecha

        # Verifica que el servicio se encuentre disponible antes de crear la reserva
        servicio.validar_disponibilidad()

        self.id = str(id_reserva).strip()
        self.cliente = cliente
        self.servicio = servicio
        self.fecha = fecha
        self.cantidad = int(cantidad)
        self.descuento = float(descuento)
        self.__estado = "PENDIENTE"
        # Calcula el costo total utilizando el método polimórfico del servicio
        self.costo_total = self.servicio.calcular_costo(self.cantidad, self.descuento)

    @property
    def estado(self) -> str:
        """Retorna el estado actual de la reserva."""
        return self.__estado

    def confirmar(self) -> None:
        """Cambia el estado de PENDIENTE a CONFIRMADA y bloquea el servicio."""
        if self.__estado != "PENDIENTE":
            raise OperacionNoPermitidaError(
                f"No se puede confirmar la reserva {self.id} porque su estado es '{self.__estado}'."
            )
        self.servicio.validar_disponibilidad()
        self.__estado = "CONFIRMADA"
        self.servicio.disponible = False

    def cancelar(self) -> None:
        """Cancela la reserva y libera nuevamente la disponibilidad del servicio."""
        if self.__estado == "CANCELADA":
            raise OperacionNoPermitidaError(f"La reserva {self.id} ya se encuentra cancelada.")
        self.__estado = "CANCELADA"
        self.servicio.disponible = True

    def obtener_resumen(self) -> str:
        """Retorna el detalle completo de la reserva."""
        return (
            f"Reserva [{self.id}] | Fecha: {self.fecha} | Estado: {self.estado} | "
            f"Cliente: {self.cliente.nombre} | Servicio: {self.servicio.nombre} | "
            f"Cant: {self.cantidad} | Total: ${self.costo_total:,.2f} COP"
        )


class GestorSoftwareFJ:
    """Administra las colecciones en memoria de clientes, servicios y reservas."""

    def __init__(self, archivo_log: str = "sistema_fj.log"):
        self.clientes: List[Cliente] = []
        self.servicios: List[Servicio] = []
        self.reservas: List[Reserva] = []
        self.logger = RegistradorLogs(archivo_log)

    def registrar_cliente(self, cliente: Cliente) -> None:
        """Agrega un cliente a la lista interna evitando IDs duplicados."""
        if any(c.id == cliente.id for c in self.clientes):
            raise DatoInvalidoError(f"Ya existe un cliente registrado con el ID '{cliente.id}'.")
        self.clientes.append(cliente)
        self.logger.registrar_evento("INFO", f"Cliente registrado: {cliente.obtener_resumen()}")

    def registrar_servicio(self, servicio: Servicio) -> None:
        """Agrega un servicio al catálogo en memoria evitando IDs duplicados."""
        if any(s.id == servicio.id for s in self.servicios):
            raise DatoInvalidoError(f"Ya existe un servicio registrado con el ID '{servicio.id}'.")
        self.servicios.append(servicio)
        self.logger.registrar_evento("INFO", f"Servicio registrado: {servicio.obtener_detalle()}")

    def crear_reserva(
        self,
        id_reserva: str,
        cliente: Cliente,
        servicio: Servicio,
        fecha: str,
        cantidad: int,
        descuento: float = 0.0,
    ) -> Reserva:
        """
        Crea una reserva encapsulando fallos de negocio mediante encadenamiento de excepciones.
        """
        try:
            nueva_reserva = Reserva(id_reserva, cliente, servicio, fecha, cantidad, descuento)
        except ErrorSistemaFJ as error_negocio:
            # Encadena la excepción específica dentro de ReservaError
            error_encadenado = ReservaError(
                f"Fallo al procesar la reserva '{id_reserva}' para {cliente.nombre}."
            )
            error_encadenado.__cause__ = error_negocio
            self.logger.registrar_error("Error en creación de reserva", error_encadenado)
            raise error_encadenado from error_negocio
        else:
            self.reservas.append(nueva_reserva)
            self.logger.registrar_evento("INFO", f"Reserva creada: {nueva_reserva.obtener_resumen()}")
            return nueva_reserva
