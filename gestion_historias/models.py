from django.db import models
from django.conf import settings

class Paciente(models.Model):
    # Información Personal Básica
    nombre = models.CharField(max_length=200, help_text="Nombre completo del paciente")
    apodo = models.CharField(max_length=100, blank=True, null=True, help_text="Apodo o alias")
    sexo = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino')], blank=True, null=True)
    edad = models.PositiveIntegerField(blank=True, null=True, help_text="Edad en años")
    fecha_nacimiento = models.DateField(blank=True, null=True)
    cedula = models.CharField(max_length=50, unique=True, help_text="Cédula/Pasaporte/NUI")

    # Información Adicional del Paciente
    aseguradora = models.CharField(max_length=100, blank=True, null=True)
    nss = models.CharField(max_length=50, blank=True, null=True, help_text="Número de Seguridad Social")
    grupo_sanguineo = models.CharField(
        max_length=3,
        choices=[
            ('O+', 'O+'), ('O-', 'O-'),
            ('A+', 'A+'), ('A-', 'A-'),
            ('B+', 'B+'), ('B-', 'B-'),
            ('AB+', 'AB+'), ('AB-', 'AB-'),
            ('', 'Desconocido')
        ],
        blank=True, null=True
    )
    peso_kg = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Peso en kilogramos")
    talla_cm = models.PositiveIntegerField(blank=True, null=True, help_text="Talla en centímetros")
    alergias = models.TextField(blank=True, null=True, help_text="Descripción de alergias conocidas")

    # Información de Contacto
    direccion = models.TextField(blank=True, null=True)
    nacionalidad = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} ({self.cedula})"

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"

class HistoriaClinicaEmergencia(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name="historias_emergencia")
    medico_tratante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="historias_atendidas"
    )

    # Información General de la Emergencia
    fecha_hora_llegada = models.DateTimeField()
    numero_expediente_clinico = models.CharField(max_length=100, blank=True, null=True)
    fecha_hora_clasificacion = models.DateTimeField(blank=True, null=True)
    PRIORIDAD_TRIAJE_CHOICES = [
        ('I', 'Nivel I - Rojo (Resucitación)'),
        ('II', 'Nivel II - Naranja (Emergencia)'),
        ('III', 'Nivel III - Amarillo (Urgencia)'),
        ('IV', 'Nivel IV - Verde (Urgencia Menor)'),
        ('V', 'Nivel V - Azul (No Urgencia)'),
    ]
    prioridad_triaje = models.CharField(max_length=3, choices=PRIORIDAD_TRIAJE_CHOICES, blank=True, null=True)
    fecha_hora_fin_clasificacion = models.DateTimeField(blank=True, null=True)

    # Vía de Llegada
    llego_medios_propios = models.BooleanField(default=False, verbose_name="Llegó por Medios Propios")
    llego_911 = models.BooleanField(default=False, verbose_name="Llegó por 9-1-1")
    llego_crue = models.BooleanField(default=False, verbose_name="Llegó por CRUE")
    llego_ambulancia_privada = models.BooleanField(default=False, verbose_name="Llegó por Ambulancia Privada")

    paramedico_responsable = models.CharField(max_length=150, blank=True, null=True)
    ambulancia_numero = models.CharField(max_length=50, blank=True, null=True)

    # Acompañante
    acompanante_nombre = models.CharField(max_length=150, blank=True, null=True)
    acompanante_parentesco = models.CharField(max_length=50, blank=True, null=True)
    acompanante_telefono = models.CharField(max_length=20, blank=True, null=True)
    acompanante_direccion = models.TextField(blank=True, null=True)

    # Motivos de la Consulta (BooleanFields)
    motivo_cefalea = models.BooleanField(default=False, verbose_name="Cefalea")
    motivo_tos = models.BooleanField(default=False, verbose_name="Tos")
    motivo_palpitaciones = models.BooleanField(default=False, verbose_name="Palpitaciones")
    motivo_hematemesis = models.BooleanField(default=False, verbose_name="Hematemesis")
    motivo_disuria = models.BooleanField(default=False, verbose_name="Disuria")
    motivo_melena = models.BooleanField(default=False, verbose_name="Melena")
    motivo_mareos = models.BooleanField(default=False, verbose_name="Mareos")
    motivo_epistaxis = models.BooleanField(default=False, verbose_name="Epistaxis")
    motivo_nauseas = models.BooleanField(default=False, verbose_name="Náuseas")
    motivo_dolor_toracico = models.BooleanField(default=False, verbose_name="Dolor torácico")
    motivo_hematuria = models.BooleanField(default=False, verbose_name="Hematuria")
    motivo_herida_arma = models.BooleanField(default=False, verbose_name="Herida de arma blanca o arma de fuego")
    motivo_vomitos = models.BooleanField(default=False, verbose_name="Vómitos")
    motivo_dolor_abdominal = models.BooleanField(default=False, verbose_name="Dolor abdominal")
    motivo_sangrado_transvaginal = models.BooleanField(default=False, verbose_name="Sangrado transvaginal")
    motivo_intoxicacion = models.BooleanField(default=False, verbose_name="Intoxicación")
    motivo_diarrea = models.BooleanField(default=False, verbose_name="Diarrea")
    motivo_disnea = models.BooleanField(default=False, verbose_name="Disnea")
    motivo_politraumatismo = models.BooleanField(default=False, verbose_name="Politraumatismo")
    motivo_tec = models.BooleanField(default=False, verbose_name="TEC (Traumatismo Encéfalo Craneano)")
    motivo_crisis_hipertensiva = models.BooleanField(default=False, verbose_name="Crisis hipertensiva")
    motivo_convulsiones = models.BooleanField(default=False, verbose_name="Convulsiones")
    motivo_quemaduras = models.BooleanField(default=False, verbose_name="Quemaduras")
    motivo_sincope = models.BooleanField(default=False, verbose_name="Síncope")
    motivo_dolor_lumbar = models.BooleanField(default=False, verbose_name="Dolor lumbar")
    motivo_otros_descripcion = models.TextField(blank=True, null=True, help_text="Especificar otros motivos")

    motivo_consulta_principal_descripcion = models.TextField(blank=True, null=True, help_text="Descripción del motivo principal de la consulta")
    enfermedad_actual_historia = models.TextField(blank=True, null=True, help_text="Historia de la enfermedad actual y cronología")

    # Antecedentes
    antecedentes_personales_patologicos = models.TextField(blank=True, null=True)
    antecedentes_quirurgicos = models.TextField(blank=True, null=True)
    antecedentes_ginecobstetricos = models.TextField(blank=True, null=True) # Considerar si es solo para F
    antecedentes_traumaticos = models.TextField(blank=True, null=True)
    antecedentes_familiares = models.TextField(blank=True, null=True)
    habitos_toxicos = models.TextField(blank=True, null=True)
    medicamentos_uso_actual = models.TextField(blank=True, null=True)

    # Revisión por Sistemas
    revision_sistemas_descripcion = models.TextField(blank=True, null=True)

    # Signos Vitales
    presion_arterial_sistolica = models.PositiveIntegerField(blank=True, null=True)
    presion_arterial_diastolica = models.PositiveIntegerField(blank=True, null=True)
    frecuencia_cardiaca_lpm = models.PositiveIntegerField(blank=True, null=True, help_text="Latidos por minuto")
    frecuencia_respiratoria_rpm = models.PositiveIntegerField(blank=True, null=True, help_text="Respiraciones por minuto")
    temperatura_celsius = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, help_text="Grados Celsius")
    saturacion_oxigeno_porc = models.PositiveIntegerField(blank=True, null=True, help_text="Porcentaje SaO2")
    glasgow_ocular = models.PositiveIntegerField(blank=True, null=True)
    glasgow_verbal = models.PositiveIntegerField(blank=True, null=True)
    glasgow_motora = models.PositiveIntegerField(blank=True, null=True)
    glasgow_total = models.PositiveIntegerField(blank=True, null=True, help_text="Suma de Glasgow (Ocular + Verbal + Motora)")
    glucometria_mg_dl = models.PositiveIntegerField(blank=True, null=True, help_text="mg/dL")

    # Examen Físico
    examen_fisico_descripcion = models.TextField(blank=True, null=True)

    # Diagnóstico
    diagnostico_presuntivo = models.TextField(blank=True, null=True)
    diagnostico_definitivo_cie10 = models.CharField(max_length=20, blank=True, null=True, help_text="Código CIE-10")
    diagnostico_definitivo_descripcion = models.TextField(blank=True, null=True)

    # Plan de Tratamiento
    plan_tratamiento_indicaciones = models.TextField(blank=True, null=True)

    # Destino del Paciente (BooleanFields)
    destino_domicilio = models.BooleanField(default=False, verbose_name="Destino: Domicilio")
    destino_sala = models.BooleanField(default=False, verbose_name="Destino: Sala")
    destino_uci = models.BooleanField(default=False, verbose_name="Destino: UCI")
    destino_quirofano = models.BooleanField(default=False, verbose_name="Destino: Quirófano")
    destino_morgue = models.BooleanField(default=False, verbose_name="Destino: Morgue")
    destino_transferencia = models.BooleanField(default=False, verbose_name="Destino: Transferencia a otra unidad")
    destino_fuga = models.BooleanField(default=False, verbose_name="Destino: Fuga")
    destino_otro = models.BooleanField(default=False, verbose_name="Destino: Otro (especificar)")
    destino_paciente_observaciones = models.TextField(blank=True, null=True, help_text="Especificar destino 'Otro' o detalles adicionales")

    # Timestamps
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Historia de Emergencia para {self.paciente.nombre if self.paciente else 'N/A'} - {self.fecha_hora_llegada.strftime('%Y-%m-%d %H:%M') if self.fecha_hora_llegada else 'N/A'}"

    class Meta:
        verbose_name = "Historia Clínica de Emergencia"
        verbose_name_plural = "Historias Clínicas de Emergencia"
        ordering = ['-fecha_hora_llegada']
