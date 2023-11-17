from django.contrib import admin
from .models import (
    UsuariosSena,
    ElementosDevolutivo,
    ElementosConsumible,
    Prestamo,
    EntregaConsumible,
)
from .choices import roles, cuentadantes


class ServicioAdmin(admin.ModelAdmin):
    readonly_fields = ("created", "update")


admin.site.register(UsuariosSena)
admin.site.register(ElementosDevolutivo)
admin.site.register(ElementosConsumible)
admin.site.register(Prestamo)
admin.site.register(EntregaConsumible)
