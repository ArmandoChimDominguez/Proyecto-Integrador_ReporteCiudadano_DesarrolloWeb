"""Errores del dominio. Los servicios los lanzan sin saber nada de HTTP;
main.py los traduce a 401/403/404/409 con el sobre de error del proyecto."""


class ErrorDominio(Exception):
    def __init__(self, mensaje: str) -> None:
        super().__init__(mensaje)
        self.mensaje = mensaje


class NoEncontrado(ErrorDominio):
    pass


class SinPermiso(ErrorDominio):
    pass


class Conflicto(ErrorDominio):
    pass


class CredencialesInvalidas(ErrorDominio):
    pass
