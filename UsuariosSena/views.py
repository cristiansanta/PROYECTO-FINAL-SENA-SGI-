from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from .forms import (
    UsuariosSenaForm,
    UserLoginForm,
    ElementosDevolutivoForm,
    PrestamosForm,
    ElementosConsumiblesForm,
    EntregaConsumibleForm,
)
from .models import (
    UsuariosSena,
    Prestamo,
    ElementosDevolutivo,
    ElementosConsumible,
    EntregaConsumible,
)
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import login, authenticate, logout
from django.core.exceptions import ValidationError
from datetime import date


# Importar biblioteca reportlab
from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.units import inch

from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Image

# Librería excel
import xlsxwriter
from datetime import datetime
from datetime import timedelta

# Create your views here.


def login_view(request):
    if request.method == "POST":
        loginForm = UserLoginForm(request.POST)
        if loginForm.is_valid():
            numeroIdentificacion = loginForm.cleaned_data.get("numeroIdentificacion")
            password = loginForm.cleaned_data.get("password")
            user = authenticate(
                request, username=numeroIdentificacion, password=password
            )

            if user is not None:
                login(request, user)
                return redirect("homedash")

            else:
                loginForm.add_error(None, "Invalid username or password")
    else:
        loginForm = UserLoginForm()

    return render(request, "indexLogin.html", {"form": loginForm})


def homedash(request):
    return render(request, "superAdmin/basedashboard.html")


def logout(request):
    return render(request, "indexLogin.html")


def consultarUsuario_view(request):
    usuarios = UsuariosSena.objects.all()  # Consulta todos los usuarios
    return render(request, "superAdmin/consultarUsuario.html", {"usuarios": usuarios})


def registroUsuario_view(request):
    if request.method == "POST":
        nombresVar = request.POST.get("nombres")
        apellidosVar = request.POST.get("apellidos")
        tipoIdentificacionVar = request.POST.get("tipoIdentificacion")
        numeroIdentificacionVar = request.POST.get("numeroIdentificacion")
        emailVar = request.POST.get("email")
        celularVar = request.POST.get("celular")
        rolVar = request.POST.get("rol")
        cuentadanteVar = request.POST.get("cuentadante")
        tipoContratoVar = request.POST.get("tipoContrato")
        is_activeVar = request.POST.get("is_active")
        duracionContratoVar = request.POST.get("duracionContrato")
        passwordVar = request.POST.get("password")
        fotoUsuarioVar = request.FILES.get(
            "fotoUsuario", None
        )  # Ajustado para manejar casos en los que no se suba una foto

        # Cifrar la contraseña
        password_cifrada = make_password(passwordVar)

        user = UsuariosSena(
            nombres=nombresVar,
            apellidos=apellidosVar,
            tipoIdentificacion=tipoIdentificacionVar,
            numeroIdentificacion=numeroIdentificacionVar,
            email=emailVar,
            celular=celularVar,
            rol=rolVar,
            cuentadante=cuentadanteVar,
            tipoContrato=tipoContratoVar,
            is_active=is_activeVar,
            # is_superuser=True, # puede hacer cualquier cosa
            is_staff=True,  # puede acceder al panel de administración, pero sus acciones específicas dentro del panel estarán limitadas por sus permisos asignados.
            duracionContrato=duracionContratoVar,
            password=password_cifrada,
            fotoUsuario=fotoUsuarioVar,
        )
        user.save()
        messages.success(request, "Usuario Registrado con Exito")

    return render(request, "superAdmin/registroUsuario.html")


def editarUsuario_view(request, id):
    try:
        user = UsuariosSena.objects.get(id=id)
        datos = {"user": user}
        # Redirigir a la vista consultarUsuario_view para recargar los datos
        return render(request, "superAdmin/editarUsuario.html", datos)
    except UsuariosSena.DoesNotExist:
        messages.warning(request, "No existe registro")
        return redirect("consultarUsuario_view")


def actualizarUsuario_view(request, id):
    if request.method == "POST":
        nombreVar = request.POST.get("nombre")
        apellidoVar = request.POST.get("apellidoo")
        tipoIdentificacionVar = request.POST.get("tipoIdentificacion")
        numeroIdentificacionVar = request.POST.get("numeroIdentificacion")
        correoSenaVar = request.POST.get("correoSena")
        celularVar = request.POST.get("celular")
        rolVar = request.POST.get("rol")
        cuentadanteVar = request.POST.get("cuentadante")
        tipoContratoVar = request.POST.get("tipoContrato")
        duracionContratoVar = request.POST.get("duracionContrato")
        estadoUsuariovar = request.POST.get("estadoUsuario")
        contraSenaVar = request.POST.get("contraSena")
        validacionContraSenaVar = request.POST.get("validacionContraSena")
        fotoUsuarioVar = request.FILES.get("fotoUsuario")

        user = UsuariosSena.objects.get(id=id)

        user.nombre = nombreVar
        user.apellidoo = apellidoVar
        user.tipoIdentificacion = tipoIdentificacionVar
        user.numeroIdentificacion = numeroIdentificacionVar
        user.correoSena = correoSenaVar
        user.celular = celularVar
        user.rol = rolVar
        user.cuentadante = cuentadanteVar
        user.tipoContrato = tipoContratoVar
        user.duracionContrato = duracionContratoVar
        user.estadoUsuario = estadoUsuariovar
        user.contraSena = contraSenaVar
        user.validacionContraSena = validacionContraSenaVar
        user.fotoUsuario = fotoUsuarioVar
        user.save()
        messages.success(request, "Usuario actualizado con Exito")  # mensaje de alerta

        # Redirigir a la vista consultarUsuario_view para recargar los datos
        return redirect("consultarUsuario_view")
    else:
        messages.warning(request, "No existe registro")
        return redirect("consultarUsuario_view")


def eliminarUsuario_view(request, id):
    try:
        user = UsuariosSena.objects.get(id=id)
        user.delete()
        messages.success(
            request, "usuario eliminado correctamente"
        )  # mensaje de alerta

        user = UsuariosSena.objects.all().values()

        # Redirigir a la vista consultarUsuario_view para recargar los datos
        return redirect("consultarUsuario_view")
    except UsuariosSena.DoesNotExist:
        messages.warning(request, "No existe registro")
        return redirect("consultarUsuario_view")


def formPrestamosDevolutivos_view(request):
    elementos = ElementosDevolutivo.objects.all().values_list(
        "nombreElemento", "serial"
    )
    usuarios = UsuariosSena.objects.all()  # Obtiene todos los ususarios
    if request.method == "POST":
        fechaDevolucionVar = request.POST.get("fechaDevolucion")

        # Convertir la fecha de devolución a un objeto date
        fechaDevolucion = date.fromisoformat(fechaDevolucionVar)
        # Manera 1 de hacerlo
        fechaEntregaVar = date.today()
        fechaDevolucionVar = request.POST.get("fechaDevolucion")
        nombreEntregavar = request.POST.get("nombreEntrega")
        nombreRecibevar = request.POST.get("nombreRecibe")
        nombreElementovar = request.POST.get("nombreElemento")
        serialSenaElementovar = request.POST.get("serialSenaElemento")
        cantidadElementoVar = int(request.POST.get("cantidadElemento"))
        valorUnidadElementoVar = int(request.POST.get("valorUnidadElemento"))
        valorTotalElementoVar = int(request.POST.get("valorTotalElemento"))
        observacionesPrestamovar = request.POST.get("observacionesPrestamo")

        try:
            elemento = ElementosDevolutivo.objects.get(
                nombreElemento=nombreElementovar, serial=serialSenaElementovar
            )

            # Validar que la cantidad no sea negativa
            if cantidadElementoVar <= 0:
                messages.error(
                    request, "La cantidad no puede ser negativa o igual a cero"
                )
                return render(request, "superAdmin/formPrestamosDevolutivos.html")

            # Validar la disponibilidad de la cantidad en el inventario
            if cantidadElementoVar > elemento.cantidadElemento:
                messages.error(
                    request, "La cantidad ingresada excede el stock disponible"
                )
                return render(request, "superAdmin/formPrestamosDevolutivos.html")
            # Comprobar si la fecha de devolución es anterior a la fecha actual
            if fechaDevolucion < date.today():
                messages.error(
                    request,
                    "La fecha de devolución no puede ser anterior a la fecha actual.",
                )
                return render(
                    request,
                    "superAdmin/formPrestamosDevolutivos.html",
                    {"elementos": elementos, "usuarios": usuarios},
                )
            # Si las validaciones son correctas, crea el objeto Prestamo
            prestamo = Prestamo(
                fechaEntrega=fechaEntregaVar,
                fechaDevolucion=fechaDevolucionVar,
                nombreEntrega=nombreEntregavar,
                nombreRecibe=nombreRecibevar,
                nombreElemento=nombreElementovar,
                serialSenaElemento=elemento,
                cantidadElemento=cantidadElementoVar,
                valorUnidadElemento=valorUnidadElementoVar,
                valorTotalElemento=valorTotalElementoVar,
                observacionesPrestamo=observacionesPrestamovar,
            )
            prestamo.save()
            messages.success(request, "Elemento Guardado Exitosamente")
        except ElementosDevolutivo.DoesNotExist:
            messages.error(
                request, "El elemento con el nombre o serial dado no existe."
            )
            return render(
                request,
                "superAdmin/formPrestamosDevolutivos.html",
                {"elementos": elementos, "usuarios": usuarios},
            )
        except ValidationError as e:
            # Manejar la excepción ValidationError
            return HttpResponse(str(e), status=400)
    return render(
        request,
        "superAdmin/formPrestamosDevolutivos.html",
        {"elementos": elementos, "usuarios": usuarios},
    )


# Rellenar serial
def get_serial_by_element_name(request):
    element_name = request.GET.get("elementName", None)
    if element_name:
        try:
            # Busca el elemento por su nombre
            elemento = ElementosDevolutivo.objects.get(nombreElemento=element_name)
            serial_number = elemento.serial
            valor_unidad = elemento.valorUnidadElemento
            stock = elemento.cantidadElemento
            return JsonResponse(
                {
                    "serialNumber": serial_number,
                    "valorUnidad": valor_unidad,
                    "Stock": stock,
                }
            )
        except ElementosDevolutivo.DoesNotExist:
            return JsonResponse({"error": "Element not found"}, status=404)
    else:
        return JsonResponse({"error": "No element name provided"}, status=400)


# Rellenar Elemento
def get_element_name_by_serial(request):
    serial_number = request.GET.get("serialNumber", None)
    if serial_number:
        try:
            # Busca el elemento por su número de serie
            elemento = ElementosDevolutivo.objects.get(serial=serial_number)
            element_name = elemento.nombreElemento
            valor_unidad = elemento.valorUnidadElemento
            stock = elemento.cantidadElemento
            return JsonResponse(
                {
                    "elementName": element_name,
                    "valorUnidad": valor_unidad,
                    "Stock": stock,
                }
            )
        except ElementosDevolutivo.DoesNotExist:
            return JsonResponse({"error": "Serial number not found"}, status=404)
    else:
        return JsonResponse({"error": "No serial number provided"}, status=400)


def formPrestamosConsumibles_view(request):
    if request.method == "POST":
        # Procesar el formulario aquí (guardar el préstamo consumible)
        nombreElementovar = request.POST.get("nombreElemento")
        cantidad_prestadavar = int(request.POST.get("cantidad_prestada"))
        # fecha_entregavar = request.POST.get("fecha_entrega")
        fecha_entregavar = date.today()  # Manera 1 de hacerlo
        serialSenaElementovar = request.POST.get("serialSenaElemento")
        nombre_solicitantevar = request.POST.get("nombre_solicitante")
        observaciones_prestamovar = request.POST.get("observaciones_prestamo")
        responsable_Entregavar = request.POST.get("responsable_Entrega")

        # instancia de PrestamoConsumible
        prestamo_consumible = EntregaConsumible(
            nombreElemento=nombreElementovar,
            cantidad_prestada=cantidad_prestadavar,
            fecha_entrega=fecha_entregavar,
            serialSenaElemento=serialSenaElementovar,
            nombre_solicitante=nombre_solicitantevar,
            observaciones_prestamo=observaciones_prestamovar,
            responsable_Entrega=responsable_Entregavar,
        )
        # Guarda la instancia en la base de datos
        prestamo_consumible.save()
    return render(request, "superAdmin/formPrestamosConsumibles.html")


def calendario(request):
    prestamos = Prestamo.objects.all()
    eventos = []

    for prestamo in prestamos:
        evento = {
            "title": prestamo.observacionesPrestamo,
            "start": prestamo.fechaEntrega.isoformat(),
            "end": (prestamo.fechaDevolucion + timedelta(days=1)).isoformat(),
        }
        eventos.append(evento)

    return render(request, "superAdmin/calendario.html", {"eventos": eventos})


def listar_prestamos(request):
    prestamos = Prestamo.objects.all()
    return render(request, "superAdmin/listarPrestamos.html", {"prestamos": prestamos})


def formElementos_view(request):
    if request.method == "POST":
        nombreElementoVar = request.POST.get("nombreElemento")
        categoriaElementoVar = request.POST.get("categoriaElemento")
        estadoElementoVar = request.POST.get("estadoElemento")
        descripcionElementoVar = request.POST.get("descripcionElemento")
        observacionElementoVar = request.POST.get("observacionElemento")
        facturaElementoVar = request.FILES.get("facturaElemento")
        cantidadElementoVar = int(request.POST.get("cantidadElemento"))
        valorUnidadElementoVar = int(request.POST.get("valorUnidadElemento"))

        # Validar que la cantidad no sea negativa
        if cantidadElementoVar <= 0:
            messages.error(request, "La cantidad no puede ser negativa o igual a cero")
            return render(request, "superAdmin/formElementos.html")

        valorTotalElementoVar = cantidadElementoVar * valorUnidadElementoVar

        if categoriaElementoVar == "D":
            serialVar = request.POST.get(
                "serialSenaElemento"
            )  # Específico para ElementosDevolutivo
            elemento = ElementosDevolutivo(
                nombreElemento=nombreElementoVar,
                categoriaElemento=categoriaElementoVar,
                estadoElemento=estadoElementoVar,
                descripcionElemento=descripcionElementoVar,
                observacionElemento=observacionElementoVar,
                cantidadElemento=cantidadElementoVar,
                valorUnidadElemento=valorUnidadElementoVar,
                valorTotalElemento=valorTotalElementoVar,
                serial=serialVar,
                facturaElemento=facturaElementoVar,
            )
        elif categoriaElementoVar == "C":
            elemento = ElementosConsumible(
                nombreElemento=nombreElementoVar,
                categoriaElemento=categoriaElementoVar,
                estadoElemento=estadoElementoVar,
                descripcionElemento=descripcionElementoVar,
                observacionElemento=observacionElementoVar,
                cantidadElemento=cantidadElementoVar,
                costoUnidadElemento=valorUnidadElementoVar,
                costoTotalElemento=valorTotalElementoVar,
                lote=request.POST.get(
                    "serialSenaElemento"
                ),  # 'lote' es como el serial en devolt.
                facturaElemento=facturaElementoVar,
            )
        else:
            messages.error(request, "Categoría de elemento no válida.")
            return render(request, "superAdmin/formElementos.html")

        elemento.save()
        messages.success(request, "Elemento Guardado Exitosamente")
        return redirect("formElementos_view")

    return render(request, "superAdmin/formElementos.html")


# ---------------------------------------------------------------------------
# def formElementos_view(request):
#     if request.method == "POST":
#         # fechaElementoVar = request.POST.get("fechaElemento")
#         nombreElementoVar = request.POST.get("nombreElemento")
#         categoriaElementoVar = request.POST.get("categoriaElemento")
#         estadoElementoVar = request.POST.get("estadoElemento")
#         cantidadElementoVar = int(request.POST.get("cantidadElemento"))
#         valorUnidadElementoVar = int(request.POST.get("valorUnidadElemento"))
#         serialVar = request.POST.get("serialSenaElemento")
#         descripcionElementoVar = request.POST.get("descripcionElemento")
#         observacionElementoVar = request.POST.get("observacionElemento")
#         facturaElementoVar = request.FILES.get(
#             "facturaElemento"
#         )  # Asumiendo que es un archivo

#         # Validar que la cantidad no sea negativa
#         if cantidadElementoVar <= 0:
#             messages.error(request, "La cantidad no puede ser negativa o igual a cero")
#             return render(request, "superAdmin/formElementos.html")

#         # Calcula el valor total
#         valorTotalElementoVar = cantidadElementoVar * valorUnidadElementoVar

#         elementos = Elementos(
#             nombreElemento=nombreElementoVar,
#             categoriaElemento=categoriaElementoVar,
#             estadoElemento=estadoElementoVar,
#             cantidadElemento=cantidadElementoVar,
#             valorUnidadElemento=valorUnidadElementoVar,
#             valorTotalElemento=valorTotalElementoVar,
#             serial=serialVar,
#             descripcionElemento=descripcionElementoVar,
#             observacionElemento=observacionElementoVar,
#             facturaElemento=facturaElementoVar,
#         )
#         elementos.save()
#         messages.success(request, "Elemento Guardado Exitosamente")

#         # Redireccionar o renderizar según sea necesario
#         return redirect("formElementos_view")

#     return render(request, "superAdmin/formElementos.html")
# ---------------------------------------------------------------------------------


def listar_elementos(request):
    elementos = ElementosDevolutivo.objects.all()
    return render(request, "superAdmin/listarElemento.html", {"elementos": elementos})


def consultarElementos(request):
    elementos = ElementosDevolutivo.objects.all()
    return render(
        request, "superAdmin/consultarElementos.html", {"elementos": elementos}
    )


def eliminarElemento(request, id):
    try:
        # Busca el objeto con el ID especificado o devuelve un error 404 si no existe
        objeto = get_object_or_404(ElementosDevolutivo, id=id)

        # Realiza la eliminación del objeto
        objeto.delete()

        messages.warning(
            request, "¿Esta Seguro Que Desea Eliminar el Elemento?"
        )  # mensaje de alerta

        # Si se elimina correctamente, devuelve una respuesta JSON con un mensaje de éxito
        # response_data = {'mensaje': 'Registro eliminado correctamente'}
        # return JsonResponse(response_data)

    except Exception as e:
        # Si se produce un error, devuelve una respuesta JSON con un mensaje de error
        messages.error(request, "No se encontro el Elemento Seleccionado")

        return redirect("consultarElementos")

    return redirect("consultarElementos")


def generar_pdf(request):
    elementos = ElementosDevolutivo.objects.all()
    elements = []
    # Crear un objeto BytesIO para almacenar el archivo PDF generado
    buffer = BytesIO()
    response = HttpResponse(content_type="application/pdf")
    response[
        "Content-Disposition"
    ] = f'attachment; filename="lista_elementos_{datetime.now().strftime("%Y%m%d%H%M%S")}.pdf"'

    custom_page_size = (21.59 * inch, 27.94 * inch)

    left_margin = 1 * inch
    right_margin = 1 * inch
    top_margin = 1 * inch
    bottom_margin = 1 * inch

    # Crear el documento PDF, usando landscape para un formato apaisado
    doc = SimpleDocTemplate(
        buffer,
        pagesize=custom_page_size,
        leftMargin=left_margin,
        rightMargin=right_margin,
        topMargin=top_margin,
        bottomMargin=bottom_margin,
    )

    # image_path = 'img/logo-sena-negro-png-2022.png'
    # logo = Image(image_path, width=1.5 * inch, height=1.5 * inch)  # Ajusta el ancho y alto de la imagen según tus necesidades
    # logo.hAlign = 'LEFT'  # Alinea la imagen a la izquierda

    data = [
        [
            "Fecha",
            "Nombre",
            "Categoría",
            "Estado",
            "Cantidad",
            "Valor Unidad",
            "Valor Total",
            "Descripción",
            "Observación",
            "Factura",
        ]
    ]
    for elemento in elementos:
        data.append(
            [
                elemento.fechaElemento,
                elemento.nombreElemento,
                elemento.categoriaElemento,
                elemento.estadoElemento,
                elemento.cantidadElemento,
                elemento.valorUnidadElemento,
                elemento.valorTotalElemento,
                elemento.descripcionElemento,
                elemento.observacionElemento,
                elemento.facturaElemento,
            ]
        )
    table = Table(data)

    row_style = TableStyle(
        [("BACKGROUND", (0, 0), (-1, 0), colors.grey)]
    )  # Color de fondo gris para la primera fila

    table.setStyle(row_style)
    title = "Lista de elementos"
    title_style = TableStyle(
        [
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 20),  # Tamaño del título
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        ]
    )
    title_data = [[title]]  # Coloca el título en una lista dentro de una lista
    title_table = Table(
        title_data, colWidths=[custom_page_size[0]]
    )  # Ancho igual al ancho de la página
    title_table.setStyle(title_style)
    style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.green),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]
    )

    # Tamaño letra
    style = TableStyle(
        [
            ("FONTSIZE", (0, 0), (-1, -1), 16),
        ]
    )
    table.setStyle(style)

    col_widths = [
        1.5 * inch,
        1.5 * inch,
        1.5 * inch,
        1.5 * inch,
        1.0 * inch,
        1.0 * inch,
        1.0 * inch,
        2.0 * inch,
        2.0 * inch,
        1.5 * inch,
    ]
    table = Table(data, colWidths=col_widths)

    # agrega la tabla al doc. y genera PDF
    # si la ruta de la imagen está activa, agregar mediante comas 'image_path'
    elements = [title_table, table]
    doc.build(elements)

    # Obtener el valor del buffer y establecerlo como la respuesta HTTP
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


def generar_excel(request):
    elementos = ElementosDevolutivo.objects.all()
    elements = []
    buffer = BytesIO()
    workbook = xlsxwriter.Workbook(buffer, {"in_memory": True})
    worksheet = workbook.add_worksheet()

    header_format = workbook.add_format(
        {"bold": True, "align": "center", "valign": "vcenter", "bg_color": "gray"}
    )
    header_format.set_border(1)

    headers = [
        "Fecha",
        "Nombre",
        "Categoría",
        "Estado",
        "Cantidad",
        "Valor Unidad",
        "Valor Total",
        "Descripción",
        "Observación",
    ]

    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header, header_format)

    # Datos de la base de datos
    for row_num, elemento in enumerate(elementos, start=1):
        worksheet.write(row_num, 0, elemento.fechaElemento)
        worksheet.write(row_num, 1, elemento.nombreElemento)
        worksheet.write(row_num, 2, elemento.categoriaElemento)
        worksheet.write(row_num, 3, elemento.estadoElemento)
        worksheet.write(row_num, 4, elemento.cantidadElemento)
        worksheet.write(row_num, 5, elemento.valorUnidadElemento)
        worksheet.write(row_num, 6, elemento.valorTotalElemento)
        worksheet.write(row_num, 7, elemento.descripcionElemento)
        worksheet.write(row_num, 8, elemento.observacionElemento)
        # worksheet.write(row_num, 9, elemento.facturaElemento)

    for col_num, header in enumerate(headers):
        worksheet.set_column(col_num, col_num, len(header) + 2)

    workbook.close()

    response = HttpResponse(content_type="application/vnd.ms-excel")
    response[
        "Content-Disposition"
    ] = f'attachment; filename="lista_elementos_{datetime.now().strftime("%Y%m%d%H%M%S")}.xlsx"'
    response.write(buffer.getvalue())
    # una región temporal de memoria
    buffer.close()
    return response
