from django import forms
from .models import Paciente, HistoriaClinicaEmergencia

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = '__all__'
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'alergias': forms.Textarea(attrs={'rows': 3}),
            'direccion': forms.Textarea(attrs={'rows': 3}),
        }

class HistoriaClinicaEmergenciaForm(forms.ModelForm):
    # Campos para fecha y hora separados que se combinarán en la vista
    fecha_llegada = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Fecha de Llegada")
    hora_llegada = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), label="Hora de Llegada")

    fecha_clasificacion = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False, label="Fecha de Clasificación")
    hora_clasificacion = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=False, label="Hora de Clasificación")

    fecha_fin_clasificacion = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False, label="Fecha Fin de Clasificación")
    hora_fin_clasificacion = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=False, label="Hora Fin de Clasificación")

    class Meta:
        model = HistoriaClinicaEmergencia
        exclude = ['paciente', 'medico_tratante', 'fecha_hora_llegada', 'fecha_hora_clasificacion', 'fecha_hora_fin_clasificacion']
        # Widgets para mejorar la apariencia o funcionalidad de campos específicos
        widgets = {
            'prioridad_triaje': forms.RadioSelect, # Para que se muestre como botones de radio
            'motivo_otros_descripcion': forms.Textarea(attrs={'rows': 2}),
            'motivo_consulta_principal_descripcion': forms.Textarea(attrs={'rows': 3}),
            'enfermedad_actual_historia': forms.Textarea(attrs={'rows': 4, 'class': 'large'}),
            'antecedentes_personales_patologicos': forms.Textarea(attrs={'rows': 3}),
            'antecedentes_quirurgicos': forms.Textarea(attrs={'rows': 3}),
            'antecedentes_ginecobstetricos': forms.Textarea(attrs={'rows': 3}),
            'antecedentes_traumaticos': forms.Textarea(attrs={'rows': 3}),
            'antecedentes_familiares': forms.Textarea(attrs={'rows': 3}),
            'habitos_toxicos': forms.Textarea(attrs={'rows': 3}),
            'medicamentos_uso_actual': forms.Textarea(attrs={'rows': 3}),
            'revision_sistemas_descripcion': forms.Textarea(attrs={'rows': 4, 'class': 'large'}),
            'examen_fisico_descripcion': forms.Textarea(attrs={'rows': 5, 'class': 'large'}),
            'diagnostico_presuntivo': forms.Textarea(attrs={'rows': 3}),
            'diagnostico_definitivo_descripcion': forms.Textarea(attrs={'rows': 3}),
            'plan_tratamiento_indicaciones': forms.Textarea(attrs={'rows': 4, 'class': 'large'}),
            'destino_paciente_observaciones': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agrupar checkboxes visualmente en el template será más fácil,
        # pero aquí podemos asegurar que los labels sean correctos si es necesario.
        # Por ejemplo, para los BooleanFields de motivos:
        field_prefix_map = {
            'llego_': "Vía de Llegada: ",
            'motivo_': "Motivo: ",
            'destino_': "Destino: "
        }
        for field_name in self.fields:
            for prefix, label_prefix in field_prefix_map.items():
                if field_name.startswith(prefix) and isinstance(self.fields[field_name], forms.BooleanField):
                    # self.fields[field_name].label = label_prefix + self.fields[field_name].label
                    pass # Django ya usa el verbose_name del modelo, que es suficiente.

        # Marcar campos de fecha/hora como no requeridos si sus contrapartes de modelo son blank=True, null=True
        # Esto se maneja mejor directamente en la definición del campo arriba con required=False

        # Asegurar que los campos de signos vitales usen NumberInput
        vital_signs_fields = [
            'presion_arterial_sistolica', 'presion_arterial_diastolica',
            'frecuencia_cardiaca_lpm', 'frecuencia_respiratoria_rpm',
            'temperatura_celsius', 'saturacion_oxigeno_porc',
            'glasgow_ocular', 'glasgow_verbal', 'glasgow_motora', 'glasgow_total',
            'glucometria_mg_dl'
        ]
        for field_name in vital_signs_fields:
            if field_name in self.fields:
                self.fields[field_name].widget = forms.NumberInput(attrs={'class': 'form-control vital-input'}) # Agregada clase para posible JS/CSS específico


    # Podríamos añadir métodos clean_ individualizados si es necesario,
    # por ejemplo, para combinar fecha y hora antes de guardar, o en la vista.
    # Por ahora, la combinación de fecha y hora se hará en la vista.

    # También podemos añadir un campo para buscar paciente existente si es necesario en el futuro.
    # O un campo para crear un nuevo paciente si no existe.
    # Por ahora, asumimos que el paciente se crea/selecciona por separado
    # y se pasa a la vista que maneja este formulario.

    # Los campos de Glasgow podrían tener validación para asegurar que son números dentro de un rango.
    # glasgow_ocular = forms.IntegerField(min_value=1, max_value=4, required=False)
    # glasgow_verbal = forms.IntegerField(min_value=1, max_value=5, required=False)
    # glasgow_motora = forms.IntegerField(min_value=1, max_value=6, required=False)
    # glasgow_total = forms.IntegerField(min_value=3, max_value=15, required=False) # Este se podría calcular
    # Por ahora, usamos los PositiveIntegerFields del modelo que ya limitan a no negativos.
    # El widget por defecto es NumberInput.


# Formulario combinado para crear Paciente e Historia en un solo paso (opcional, más complejo de manejar en la vista)
# class CombinedPacienteHistoriaForm(forms.Form):
#     # Campos de Paciente
#     nombre_paciente = forms.CharField(label="Nombre del Paciente")
#     cedula_paciente = forms.CharField(label="Cédula del Paciente")
#     # ... otros campos de paciente ...
#
#     # Campos de Historia
#     fecha_llegada = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
#     hora_llegada = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
#     # ... otros campos de historia ...
#
#     def save(self):
#         # Lógica para crear o obtener paciente, luego crear historia.
#         pass
