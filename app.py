from spyne import (
    Application,
    rpc,
    ServiceBase,
    Unicode,
    ComplexModel
)

from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication


# =====================================================
# MODELO DE DATOS
# =====================================================

class Paciente(ComplexModel):
    idPaciente = Unicode
    nombre = Unicode
    documento = Unicode
    estado = Unicode


# =====================================================
# DATOS SIMULADOS DEL HOSPITAL
# =====================================================

pacientes = {
    "P001": {
        "nombre": "Maria Perez",
        "documento": "1001001001",
        "estado": "ACTIVO"
    },

    "P002": {
        "nombre": "Carlos Gomez",
        "documento": "1002002002",
        "estado": "ACTIVO"
    },

    "P003": {
        "nombre": "Ana Torres",
        "documento": "1003003003",
        "estado": "INACTIVO"
    }
}


# =====================================================
# SERVICIO SOAP
# =====================================================

class ServicioPacientes(ServiceBase):

    @rpc(
        Unicode,
        _returns=Paciente
    )
    def consultarPaciente(ctx, idPaciente):

        if idPaciente in pacientes:

            datos = pacientes[idPaciente]

            return Paciente(
                idPaciente=idPaciente,
                nombre=datos["nombre"],
                documento=datos["documento"],
                estado=datos["estado"]
            )

        return Paciente(
            idPaciente=idPaciente,
            nombre="NO ENCONTRADO",
            documento="",
            estado="NO EXISTE"
        )


    @rpc(
        Unicode,
        _returns=Unicode
    )
    def consultarEstadoPaciente(ctx, idPaciente):

        if idPaciente in pacientes:
            return pacientes[idPaciente]["estado"]

        return "PACIENTE NO ENCONTRADO"


    @rpc(
        Unicode,
        Unicode,
        Unicode,
        _returns=Unicode
    )
    def registrarPaciente(ctx, idPaciente, nombre, documento):

        if idPaciente in pacientes:
            return "ERROR: El paciente ya existe"

        pacientes[idPaciente] = {
            "nombre": nombre,
            "documento": documento,
            "estado": "ACTIVO"
        }

        return "PACIENTE REGISTRADO CORRECTAMENTE"


    @rpc(
        Unicode,
        Unicode,
        _returns=Unicode
    )
    def actualizarPaciente(ctx, idPaciente, estado):

        if idPaciente not in pacientes:
            return "ERROR: Paciente no encontrado"

        pacientes[idPaciente]["estado"] = estado

        return "PACIENTE ACTUALIZADO CORRECTAMENTE"


# =====================================================
# APLICACION SOAP
# =====================================================

soap_app = Application(

    [ServicioPacientes],

    tns="hospital.servicios.pacientes",

    in_protocol=Soap11(
        validator="lxml"
    ),

    out_protocol=Soap11()
)


# =====================================================
# APLICACION WSGI
# =====================================================

app = WsgiApplication(soap_app)
