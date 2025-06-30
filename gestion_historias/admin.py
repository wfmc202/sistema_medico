from django.contrib import admin
from .models import Paciente, HistoriaClinicaEmergencia

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cedula', 'edad', 'sexo', 'fecha_nacimiento', 'telefono')
    search_fields = ('nombre', 'cedula')
    list_filter = ('sexo', 'grupo_sanguineo')
    ordering = ('nombre',)

@admin.register(HistoriaClinicaEmergencia)
class HistoriaClinicaEmergenciaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'fecha_hora_llegada', 'prioridad_triaje', 'medico_tratante', 'numero_expediente_clinico')
    search_fields = ('paciente__nombre', 'paciente__cedula', 'numero_expediente_clinico', 'medico_tratante__username')
    list_filter = ('prioridad_triaje', 'fecha_hora_llegada', 'medico_tratante')
    ordering = ('-fecha_hora_llegada',)

    # Para campos de fecha y hora, es útil tenerlos separados en el admin si no se usa un widget específico
    # readonly_fields = ('fecha_creacion', 'fecha_actualizacion') # Ya son auto_now y auto_now_add

    fieldsets = (
        ("Información General", {
            'fields': ('paciente', 'medico_tratante',
                       ('fecha_hora_llegada', 'numero_expediente_clinico'),
                       ('fecha_hora_clasificacion', 'prioridad_triaje'),
                       'fecha_hora_fin_clasificacion')
        }),
        ("Vía de Llegada y Acompañante", {
            'fields': (('llego_medios_propios', 'llego_911', 'llego_crue', 'llego_ambulancia_privada'),
                       'paramedico_responsable', 'ambulancia_numero',
                       'acompanante_nombre', 'acompanante_parentesco', 'acompanante_telefono', 'acompanante_direccion')
        }),
        ("Motivos de Consulta", {
            'fields': tuple(f'motivo_{m}' for m in ['cefalea', 'tos', 'palpitaciones', 'hematemesis', 'disuria', 'melena', 'mareos', 'epistaxis', 'nauseas', 'dolor_toracico', 'hematuria', 'herida_arma', 'vomitos', 'dolor_abdominal', 'sangrado_transvaginal', 'intoxicacion', 'diarrea', 'disnea', 'politraumatismo', 'tec', 'crisis_hipertensiva', 'convulsiones', 'quemaduras', 'sincope', 'dolor_lumbar']) + ('motivo_otros_descripcion', 'motivo_consulta_principal_descripcion', 'enfermedad_actual_historia')
        }),
        ("Antecedentes", {
            'fields': ('antecedentes_personales_patologicos', 'antecedentes_quirurgicos', 'antecedentes_ginecobstetricos', 'antecedentes_traumaticos', 'antecedentes_familiares', 'habitos_toxicos', 'medicamentos_uso_actual')
        }),
        ("Revisión por Sistemas y Examen Físico", {
            'fields': ('revision_sistemas_descripcion', 'examen_fisico_descripcion')
        }),
        ("Signos Vitales y Glasgow", {
            'fields': (('presion_arterial_sistolica', 'presion_arterial_diastolica'),
                       ('frecuencia_cardiaca_lpm', 'frecuencia_respiratoria_rpm'),
                       ('temperatura_celsius', 'saturacion_oxigeno_porc'),
                       'glucometria_mg_dl',
                       ('glasgow_ocular', 'glasgow_verbal', 'glasgow_motora', 'glasgow_total'))
        }),
        ("Diagnóstico y Plan", {
            'fields': ('diagnostico_presuntivo',
                       ('diagnostico_definitivo_cie10', 'diagnostico_definitivo_descripcion'),
                       'plan_tratamiento_indicaciones')
        }),
        ("Destino del Paciente", {
            'fields': tuple(f'destino_{d}' for d in ['domicilio', 'sala', 'uci', 'quirofano', 'morgue', 'transferencia', 'fuga', 'otro']) + ('destino_paciente_observaciones',)
        }),
        ("Timestamps", {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',), # Opcional: colapsar esta sección
        }),
    )

    # Si los BooleanFields para motivos y destino son muchos, el fieldset puede ser largo.
    # Alternativamente, se pueden listar en `fields` directamente o usar filter_horizontal/vertical para ManyToMany si se cambia el modelo.
    # Para BooleanFields, la representación por defecto es un checkbox, lo cual es adecuado.

    def get_queryset(self, request):
        # Optimizar la carga de datos relacionados
        return super().get_queryset(request).select_related('paciente', 'medico_tratante')

# Considerar registrar otros modelos si es necesario, por ejemplo, un perfil de médico si se crea.
