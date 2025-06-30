from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Paciente, HistoriaClinicaEmergencia
from .forms import PacienteForm, HistoriaClinicaEmergenciaForm
from django.utils.dateparse import parse_datetime
from django.conf import settings
import datetime # Asegúrate de importar datetime

# TODO: Implementar una vista para listar pacientes y seleccionar uno, o crear uno nuevo.
# Por ahora, la creación de historia asumirá que el paciente ya existe o se crea inline.

@login_required
def crear_historia_clinica(request):
    if request.method == 'POST':
        paciente_form = PacienteForm(request.POST, prefix="pac")
        historia_form = HistoriaClinicaEmergenciaForm(request.POST, prefix="hist")

        if paciente_form.is_valid() and historia_form.is_valid():
            # Intentar obtener el paciente por cédula, si no, crear uno nuevo
            cedula = paciente_form.cleaned_data.get('cedula')
            paciente, created = Paciente.objects.get_or_create(
                cedula=cedula,
                defaults=paciente_form.cleaned_data
            )
            if not created: # Si el paciente ya existía, actualizar sus datos si es necesario
                for attr, value in paciente_form.cleaned_data.items():
                    setattr(paciente, attr, value)
                paciente.save()

            historia = historia_form.save(commit=False)
            historia.paciente = paciente
            historia.medico_tratante = request.user

            # Combinar fecha y hora para los campos DateTimeField del modelo
            try:
                fecha_llegada = historia_form.cleaned_data.get('fecha_llegada')
                hora_llegada = historia_form.cleaned_data.get('hora_llegada')
                if fecha_llegada and hora_llegada:
                    historia.fecha_hora_llegada = datetime.datetime.combine(fecha_llegada, hora_llegada)

                fecha_clasificacion = historia_form.cleaned_data.get('fecha_clasificacion')
                hora_clasificacion = historia_form.cleaned_data.get('hora_clasificacion')
                if fecha_clasificacion and hora_clasificacion:
                    historia.fecha_hora_clasificacion = datetime.datetime.combine(fecha_clasificacion, hora_clasificacion)

                fecha_fin_clasificacion = historia_form.cleaned_data.get('fecha_fin_clasificacion')
                hora_fin_clasificacion = historia_form.cleaned_data.get('hora_fin_clasificacion')
                if fecha_fin_clasificacion and hora_fin_clasificacion:
                    historia.fecha_hora_fin_clasificacion = datetime.datetime.combine(fecha_fin_clasificacion, hora_fin_clasificacion)

            except Exception as e:
                messages.error(request, f"Error al procesar fechas y horas: {e}")
                # Considerar qué hacer si hay un error aquí, quizás renderizar el form de nuevo con el error.
                # Por ahora, se guardará con los campos de fecha/hora que se hayan podido procesar.

            historia.save()
            messages.success(request, f"Historia clínica para {paciente.nombre} creada exitosamente.")
            return redirect('detalle_historia_clinica', historia_id=historia.id) # Asumiendo que tendrás esta vista

    else:
        paciente_form = PacienteForm(prefix="pac")
        historia_form = HistoriaClinicaEmergenciaForm(prefix="hist")

    context = {
        'paciente_form': paciente_form,
        'historia_form': historia_form,
        'template_path': 'gestion_historias/base_form.html' # Para pasar al template base
    }
    # Usaremos la plantilla base.html directamente por ahora, adaptándola para Django.
    # Idealmente, tendríamos una plantilla específica para esta vista.
    return render(request, 'gestion_historias/crear_historia_clinica.html', context)


@login_required
def detalle_historia_clinica(request, historia_id):
    historia = get_object_or_404(HistoriaClinicaEmergencia, id=historia_id)
    context = {
        'historia': historia,
        'paciente': historia.paciente,
    }
    return render(request, 'gestion_historias/detalle_historia_clinica.html', context)


@login_required
def listar_historias_clinicas(request):
    historias = HistoriaClinicaEmergencia.objects.all().order_by('-fecha_hora_llegada') # O la ordenación que prefieras
    context = {
        'historias': historias
    }
    return render(request, 'gestion_historias/listar_historias_clinicas.html', context)

# Placeholder para vistas futuras:
# def editar_historia_clinica(request, historia_id):
#     pass

# def buscar_paciente(request):
#     pass
