from django.db import models
from django.utils.html import format_html
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from .choices import (
    roles,
    cuentadantes,
    estado,
    categoriaElemento,
    tipoId,
    tipoContratos,
)


class UsuariosSenaManager(BaseUserManager):
    def create_user(self, numeroIdentificacion, email, password=None, **extra_fields):
        user = self.model(
            numeroIdentificacion=numeroIdentificacion,
            email=self.normalize_email(email),
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, numeroIdentificacion, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(numeroIdentificacion, email, password, **extra_fields)


class UsuariosSena(AbstractUser):
    nombres = models.CharField(max_length=25)
    apellidos = models.CharField(max_length=25)
    tipoIdentificacion = models.CharField(max_length=25, choices=tipoId, default="CC")
    numeroIdentificacion = models.CharField(max_length=25, unique=True)
    email = models.EmailField(max_length=25)
    celular = models.CharField(max_length=10)
    rol = models.CharField(max_length=25, choices=roles, default="I")
    cuentadante = models.CharField(
        max_length=25, choices=cuentadantes, default="adminD"
    )
    tipoContrato = models.CharField(max_length=25, choices=tipoContratos, default="P")
    is_active = models.BooleanField(default=1)
    duracionContrato = models.CharField(max_length=25)
    password = models.CharField(max_length=30, default="")
    fotoUsuario = models.ImageField(
        upload_to="usuarioFoto/", blank=True, null=True
    )  # Campo para la foto
    id = models.BigAutoField(primary_key=True)

    objects = UsuariosSenaManager()

    username = None
    last_name = None
    first_name = None

    # Set the node for log in
    USERNAME_FIELD = "numeroIdentificacion"


class ElementosDevolutivo(models.Model):
    fechaElemento = models.DateField(auto_now_add=True)  # Manera 2 de hacerlo
    nombreElemento = models.CharField(max_length=25)
    categoriaElemento = models.CharField(
        max_length=25, choices=categoriaElemento, default="C"
    )
    estadoElemento = models.CharField(max_length=25, choices=estado, default="D")
    descripcionElemento = models.CharField(max_length=25)
    observacionElemento = models.CharField(max_length=25)

    cantidadElemento = models.IntegerField()
    valorUnidadElemento = models.IntegerField()
    valorTotalElemento = models.IntegerField(blank=True, null=True)
    serial = models.CharField(max_length=25, primary_key=True)
    facturaElemento = models.ImageField(
        upload_to="facturaElemento/", blank=True, null=True
    )  # Campo para la foto

    def __str__(self):
        return f"Elemento devolutivo {self.nombreElemento}, unidades disponibles {self.cantidadElemento}"


class ElementosConsumible(models.Model):
    fechaAdquisicion = models.DateField(auto_now_add=True)
    nombreElemento = models.CharField(max_length=25)
    categoriaElemento = models.CharField(
        max_length=25, choices=[("D", "Devolutivo"), ("C", "Consumible")], default="C"
    )
    estadoElemento = models.CharField(
        max_length=25, choices=[("D", "Disponible"), ("A", "Agotado")], default="D"
    )
    descripcionElemento = models.CharField(max_length=25)
    observacionElemento = models.CharField(max_length=25)

    cantidadElemento = models.IntegerField()
    costoUnidadElemento = models.IntegerField()
    costoTotalElemento = models.IntegerField(blank=True, null=True)
    lote = models.CharField(max_length=25)
    facturaElemento = models.ImageField(
        upload_to="facturaElemento/", blank=True, null=True
    )

    def __str__(self):
        return f"Elemento consumible {self.nombreElemento}, unidades disponibles {self.cantidadElemento}"


class Prestamo(models.Model):
    fechaEntrega = models.DateField()
    fechaDevolucion = models.DateField()
    nombreEntrega = models.CharField(max_length=25)
    nombreRecibe = models.CharField(max_length=25, null=False)
    nombreElemento = models.CharField(max_length=25)
    estado = models.CharField(max_length=10, default="ACTIVO")
    serialSenaElemento = models.ForeignKey(
        ElementosDevolutivo, on_delete=models.CASCADE, related_name="prestamos"
    )
    cantidadElemento = models.IntegerField()
    valorUnidadElemento = models.IntegerField()
    valorTotalElemento = models.IntegerField(blank=True, null=True)
    firmaDigital = models.ImageField(
        upload_to="firmaDigital/", blank=True, null=True
    )  # Campo para la foto
    observacionesPrestamo = models.CharField(max_length=25)
    id = models.BigAutoField(primary_key=True)

    def __str__(self):
        return f"Prestamo devolutivo de {self.cantidadElemento} unidades de {self.nombreElemento}"


class EntregaConsumible(models.Model):
    fecha_entrega = models.DateField()
    responsable_Entrega = models.CharField(max_length=25)
    nombre_solicitante = models.CharField(max_length=100)
    nombreElemento = models.CharField(max_length=25)
    serialSenaElemento = models.CharField(max_length=100)
    cantidad_prestada = models.PositiveIntegerField()
    observaciones_prestamo = models.TextField()
    firmaDigital = models.ImageField(
        upload_to="firmaDigital/", blank=True, null=True
    )  # Campo para la foto
    id = models.BigAutoField(primary_key=True)

    def __str__(self):
        return self.nombreElemento
