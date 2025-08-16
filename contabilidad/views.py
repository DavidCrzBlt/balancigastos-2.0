from django.shortcuts import render, redirect, get_object_or_404
from .forms import GastosVehiculosForm, GastosGeneralesForm, GastosMaterialesForm, GastosManoObraForm, GastosSeguridadForm, GastosEquiposForm, IngresosForm
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from .models import GastosVehiculos, GastosGenerales, GastosMateriales, GastosManoObra, GastosEquipos, GastosSeguridad, Ingresos
from proyectos.models import Proyectos
from empleados.models import Salario
from django.db.models import Sum, F
from django.db.models.functions import Coalesce, ExtractWeek, ExtractYear
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from decimal import Decimal
from django.contrib import messages
from .models import Gasto, CategoriaGasto
from .forms import GastoForm, CategoriaGastoForm, NominaEmpleadoForm
from contabilidad.utils import calcular_iva, recalcular_totales_proyecto
from contabilidad.mixins import ProyectoOperacionMixin
from django.urls import reverse

import pandas as pd


from .models import NominaEmpleado, Lote, Gasto, CategoriaGasto

# Create your views here.

### Vistas de detalle de proyecto ------------------------------------------- ###
### Funciones genéricas para registro, edición y eliminación de instancias--- ###
### Funciones de registro y edición de instancias por tipo de gasto o ingreso ###
### Funciones de eliminación de instancias ---------------------------------- ###

### ------------------------------------------------------------------------- ###
### ------------------------------------------------------------------------- ###
# Se muestran todas las vistas de los detalles del proyecto
### ------------------------------------------------------------------------- ###
### ------------------------------------------------------------------------- ###


class ListaGastosView(LoginRequiredMixin, ListView):
    model = Gasto
    template_name = 'contabilidad/gastos.html'
    context_object_name = 'gastos'

    def get_queryset(self):
        proyecto = Proyectos.objects.get(slug=self.kwargs['slug'])
        return Gasto.objects.filter(proyecto=proyecto).order_by('-fecha')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        proyecto = Proyectos.objects.get(slug=slug)

        context.update({
            'page_title': f'Lista de gastos {proyecto}',
            'proyecto': proyecto,
            'active_tab': 'gastos',
            'mostrar_tabs': True,
        })
        return context


class ListaCategoriasGastoView(LoginRequiredMixin, ListView):
    model = CategoriaGasto
    template_name = 'contabilidad/lista_categorias.html'
    context_object_name = 'categorias'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Categorías de gasto'
        return context
    
class ListaNominasView(LoginRequiredMixin, ListView):
    model = NominaEmpleado
    template_name = 'contabilidad/nominas_list.html'
    context_object_name = 'nominas'

    def get_queryset(self):
        proyecto = Proyectos.objects.get(slug=self.kwargs['slug'])
        return NominaEmpleado.objects.filter(proyecto=proyecto).order_by('-fecha')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        proyecto = Proyectos.objects.get(slug=slug)
        context.update({
            'page_title': f'Lista de nóminas {proyecto}',
            'proyecto': proyecto,
            'active_tab': 'nóminas',
            'mostrar_tabs': True,
        })
        return context


class IngresosListView(LoginRequiredMixin,ListView):
    model = Ingresos
    template_name = "contabilidad/ingresos.html"

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        proyecto = Proyectos.objects.get(slug=slug)
        return Ingresos.objects.filter(proyecto=proyecto)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        proyecto = Proyectos.objects.get(slug=slug)

        # Calculate total monto using aggregate
        total_monto = Ingresos.objects.filter(proyecto=proyecto).aggregate(total=Sum('monto'))['total'] or 0

        # Calculate total iva using aggregate
        total_iva = Ingresos.objects.filter(proyecto=proyecto).aggregate(total=Sum('iva'))['total'] or 0

        # Add the total to the context
        context.update({
            'page_title': f'Lista de ingresos {proyecto}',
            'proyecto': proyecto,
            'total_monto': total_monto,
            'total_iva': total_iva,
            'active_tab': 'ingresos',
            'mostrar_tabs': True,
        })
        return context 
    
### ------------------------------------------------------------------------- ###
### ------------------------------------------------------------------------- ###
# Escribimos dos funciones que vamos a reutilizar después
### ------------------------------------------------------------------------- ###
### ------------------------------------------------------------------------- ###

# Recalcular gastos e ingresos por fecha. Esto se usará para detalle de proyecto después.
def recalcular_ingresos_gastos_por_fecha(proyecto_id):

    # Obtener ingresos agrupados por año y semana
    ingresos_semanales = (
        Ingresos.objects
        .filter(proyecto_id=proyecto_id)
        .annotate(semana=ExtractWeek('fecha'), año=ExtractYear('fecha'))
        .values('año', 'semana')
        .annotate(total_ingresos=Sum('monto'))
        .order_by('año', 'semana')
    )

    df_ingresos = pd.DataFrame(columns=['fecha','total_ingresos'])

    if ingresos_semanales.exists():
        # Calcular la fecha correspondiente a cada año y semana
        for ingreso in ingresos_semanales:
            año = ingreso['año']
            semana = ingreso['semana']
            fecha = f'{año}-w{semana}'
            total_ingresos = ingreso['total_ingresos']

            # Agregar los datos al df
            df_ingresos.loc[len(df_ingresos)] = [fecha,total_ingresos]
            
    # Definir todas las tablas de gastos a considerar
    tablas_gastos = [GastosVehiculos, GastosGenerales, GastosMateriales, GastosSeguridad, GastosManoObra, GastosEquipos]

    df_gastos = pd.DataFrame(columns=['fecha','total_gastos'])

    # Iterar sobre cada tabla de gastos, obtener los datos y agregarlos
    for tabla in tablas_gastos:
        # Obtener ingresos agrupados por año y semana
        gastos_semanales = (
            tabla.objects
            .filter(proyecto_id=proyecto_id)
            .annotate(semana=ExtractWeek('fecha'), año=ExtractYear('fecha'))
            .values('año','semana')
            .annotate(total_gastos=Sum('monto'))
            .order_by('año', 'semana')
        ) 
        
        if gastos_semanales.exists():  # Solo si hay gastos en esa categoría

            for gasto in gastos_semanales:
                año = gasto['año']
                semana = gasto['semana']
                fecha = f'{año}-w{semana}'
                total_gastos = gasto['total_gastos']

                # Buscar si existe la fecha
                filtro = df_gastos[df_gastos['fecha'] == fecha]

                # Si la búsqueda de fecha encontró una coincidencia
                if not filtro.empty:
                    i = filtro.index[0] # Encuentra el índice de la fecha
                    df_gastos['total_gastos'].loc[i] += total_gastos #Sumar los gastos
                else:
                    # Crear un nuevo dato si no existe
                    df_gastos.loc[len(df_gastos)] = [fecha,total_gastos]

    # Unir los dataframes usando la columna fecha
    df_semanal = pd.merge(df_ingresos,df_gastos,on='fecha',how='outer')

    # Asegurarte de que ambas columnas sean numéricas
    df_semanal['total_ingresos'] = pd.to_numeric(df_semanal['total_ingresos'], errors='coerce')
    df_semanal['total_gastos'] = pd.to_numeric(df_semanal['total_gastos'], errors='coerce')

    # Reemplazar NaN por 0 en los que no tengan valores
    df_semanal.fillna(0, inplace=True)

    # Separar el año y la semana
    df_semanal[['año', 'semana']] = df_semanal['fecha'].str.extract(r'(\d{4})-w(\d{2})')
    df_semanal['año'] = df_semanal['año'].astype(int)
    df_semanal['semana'] = df_semanal['semana'].astype(int)

    # Convertir a fecha correspondiente al domingo de esa semana (cambiamos a 7 en lugar de 1)
    df_semanal['fecha'] = pd.to_datetime(df_semanal['año'].astype(str) + df_semanal['semana'].astype(str) + '7', format='%G%V%u')

    # Ordenar el DataFrame por la columna de 'fecha'
    df_semanal = df_semanal.sort_values('fecha')
    df_semanal.set_index('fecha',inplace=True)
    df_semanal.drop(columns=['año','semana'], inplace=True)
    
    return df_semanal


# Recalcular los totales de ingresos y gastos para el proyecto
def recalcular_totales_proyecto(proyecto_id):
    proyecto = Proyectos.objects.get(id=proyecto_id)

    ingresos_result = Ingresos.objects.filter(proyecto=proyecto).aggregate(
        total_ingresos=Coalesce(Sum('monto'),Decimal('0.00')),
        total_iva = Coalesce(Sum('iva'),Decimal('0.00'))
        )
    total_ingresos = ingresos_result['total_ingresos'] 
    total_iva_ingresos = ingresos_result['total_iva']

    gastos_vehiculos_result = GastosVehiculos.objects.filter(proyecto=proyecto).aggregate(
        total_gastos_vehiculos=Coalesce(Sum('monto'),Decimal('0.00')),
        total_iva_vehiculos = Coalesce(Sum('iva'),Decimal('0.00'))
        )
    gastos_vehiculos = gastos_vehiculos_result['total_gastos_vehiculos']
    iva_vehiculos = gastos_vehiculos_result['total_iva_vehiculos']

    gastos_generales_result = GastosGenerales.objects.filter(proyecto=proyecto).aggregate(
        total_gastos_generales=Coalesce(Sum('monto'),Decimal('0.00')),
        total_iva_generales=Coalesce(Sum('iva'),Decimal('0.00'))
        )
    gastos_generales = gastos_generales_result['total_gastos_generales'] 
    iva_generales = gastos_generales_result['total_iva_generales'] 

    gastos_materiales_result = GastosMateriales.objects.filter(proyecto=proyecto).aggregate(
        total_gastos_materiales=Coalesce(Sum('monto'),Decimal('0.00')),
        total_iva_materiales=Coalesce(Sum('iva'),Decimal('0.00'))
        )
    gastos_materiales = gastos_materiales_result['total_gastos_materiales'] 
    iva_materiales = gastos_materiales_result['total_iva_materiales'] 

    gastos_seguridad_result = GastosSeguridad.objects.filter(proyecto=proyecto).aggregate(
        total_gastos_seguridad=Coalesce(Sum('monto'),Decimal('0.00')),
        total_iva_seguridad=Coalesce(Sum('iva'),Decimal('0.00'))
        )
    gastos_seguridad = gastos_seguridad_result['total_gastos_seguridad']
    iva_seguridad = gastos_seguridad_result['total_iva_seguridad']

    gastos_mano_obra_result = GastosManoObra.objects.filter(proyecto=proyecto).aggregate(total_gastos_mano_obra=Coalesce(Sum('monto'),Decimal('0.00')))
    gastos_mano_obra = gastos_mano_obra_result['total_gastos_mano_obra'] 

    gastos_equipos_result = GastosEquipos.objects.filter(proyecto=proyecto).aggregate(
        total_gastos_equipos=Coalesce(Sum('monto'),Decimal('0.00')),
        total_iva_equipos=Coalesce(Sum('iva'),Decimal('0.00'))
        )
    gastos_equipos = gastos_equipos_result['total_gastos_equipos'] 
    iva_equipos = gastos_equipos_result['total_iva_equipos'] 

    # Add the numerical results
    total_gastos = gastos_vehiculos + gastos_generales + gastos_materiales + gastos_mano_obra + gastos_equipos + gastos_seguridad

    total_iva_gastos = iva_vehiculos + iva_generales + iva_materiales + iva_equipos + iva_seguridad

    # Actualizar el proyecto con los nuevos valores
    total_neto = total_ingresos - total_gastos
    iva_neto = total_iva_ingresos - total_iva_gastos

    # Actualizar el proyecto con los nuevos valores
    proyecto.total = total_neto
    proyecto.iva = iva_neto
    proyecto.save()

    # Retornar un diccionario con los valores calculados
    return {
        'total_ingresos': total_ingresos,
        'total_iva_ingresos': total_iva_ingresos,
        'total_gastos': total_gastos,
        'total_iva_gastos': total_iva_gastos,
        'gastos_vehiculos':gastos_vehiculos,
        'iva_vehiculos':iva_vehiculos,
        'gastos_generales':gastos_generales,
        'iva_generales':iva_generales,
        'gastos_materiales':gastos_materiales,
        'iva_materiales':iva_materiales,
        'gastos_seguridad':gastos_seguridad,
        'iva_seguridad':iva_seguridad,
        'gastos_equipos':gastos_equipos,
        'iva_equipos':iva_equipos,
        'gastos_mano_obra':gastos_mano_obra,
        'total_neto': total_neto,
        'iva_neto': iva_neto
    }


@login_required
def eliminar_operaciones_generico(request,slug,modelo,instancia_id,redirect_url):
    # Obtener el proyecto
    proyecto = get_object_or_404(Proyectos, slug=slug)

    if proyecto.estatus == True:

        # Buscar el movimiento por ID
        movimiento = get_object_or_404(modelo, id=instancia_id, proyecto=proyecto)

        # Eliminar el movimiento
        movimiento.delete()

        # Actualizar el valor neto del proyecto (suma o resta según la categoría)
        recalcular_totales_proyecto(proyecto.id)

        # Mostrar un mensaje de éxito
        messages.success(request, 'El gasto ha sido eliminado exitosamente.')

        # Redirigir a la lista de gastos o a la página que prefieras
        return redirect(redirect_url, slug=slug)
    else:
        # Mostrar un mensaje de advertencia
        messages.error(request, 'No se pueden hacer cambios a un proyecto inactivo.')
        # Redirigir a página de error
        return redirect(redirect_url,slug=slug)

### ------------------------------------------------------------------------- ###
### ------------------------------------------------------------------------- ###
# A partir de aquí se registran los gastos e ingresos
### ------------------------------------------------------------------------- ###
### ------------------------------------------------------------------------- ###

class CrearIngresoView(LoginRequiredMixin, ProyectoOperacionMixin, CreateView):
    model = Ingresos
    form_class = IngresosForm
    template_name = 'form_template.html'

    def get_success_url(self):
        return reverse('contabilidad:ingresos', kwargs={'slug': self.proyecto.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'form_title': f'Registrar ingreso {self.proyecto}',
            'button_text': 'Guardar ingreso',
            'page_title': f'Registro de ingresos {self.proyecto}',
            'proyecto': self.proyecto,
            'active_tab': 'ingresos',
            'mostrar_tabs': True,
        })
        return context


class CrearGastoView(LoginRequiredMixin, ProyectoOperacionMixin, CreateView):
    model = Gasto
    form_class = GastoForm
    template_name = 'form_template.html'

    def get_success_url(self):
        return reverse('contabilidad:gastos', kwargs={'slug': self.proyecto.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'form_title': f'Registrar gasto {self.proyecto}',
            'button_text': 'Guardar gasto',
            'page_title': f'Registro de gastos {self.proyecto}',
            'proyecto': self.proyecto,
            'active_tab': 'gastos',
            'mostrar_tabs': True,
        })

        return context
    
class CrearNominaView(CreateView):
    model = NominaEmpleado
    form_class = NominaEmpleadoForm
    template_name = 'form_template.html'

    def dispatch(self, request, *args, **kwargs):
        self.proyecto = get_object_or_404(Proyectos, slug=self.kwargs['slug'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Crear un lote automáticamente
        lote = Lote.objects.create(proyecto=self.proyecto)

        nomina = form.save(commit=False)
        nomina.lote = lote
        nomina.proyecto = self.proyecto
        nomina.save()

        # Crear gasto asociado
        categoria = CategoriaGasto.objects.get(nombre="Mano de Obra")
        Gasto.objects.create(
            proyecto=self.proyecto,
            categoria=categoria,
            concepto = f"Mano de Obra/Lote: {lote}",
            monto=nomina.total,
            iva=Decimal('0.00'),
            fecha=nomina.fecha,
            descripcion=f"Nómina para {nomina.empleado} en lote {lote.id}",
            lote=lote
        )

        # Recalcular totales del proyecto
        recalcular_totales_proyecto(self.proyecto.id)

        messages.success(self.request, "Nómina registrada exitosamente.")
        return redirect('contabilidad:nominas', slug=self.proyecto.slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form_title': f'Registrar nómina {self.proyecto}',
            'button_text': 'Guardar nómina',
            'page_title': f'Registro de nóminas {self.proyecto}',
            'proyecto': self.proyecto,
            'active_tab': 'nóminas',
            'mostrar_tabs': True,
        })
        return context


class CrearCategoriaGastoView(LoginRequiredMixin, CreateView):
    model = CategoriaGasto
    form_class = CategoriaGastoForm
    template_name = 'form_template.html'
    
    def get_success_url(self):
        return reverse('contabilidad:categorias_gasto')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form_title': 'Agregar categoría de gasto',
            'button_text': 'Crear categoría',
            'page_title': 'Nueva categoría',
        })
        return context


### ------------------------------------------------------------------------- ###
### ------------------------------------------------------------------------- ###
# A partir de aquí se eliminan instancias de gastos o ingresos
### ------------------------------------------------------------------------- ###
### ------------------------------------------------------------------------- ###

@login_required
def eliminar_gastos_mano_obra(request,slug,gasto_id):

    # Obtenemos el proyecto
    proyecto = Proyectos.objects.get(slug=slug)
    # No se pueden hacer cambios a proyectos inactivos
    if proyecto.estatus == True:
        # También tenemos que eliminar los salarios de la tabla Salario en empleados
        # Para eso necesitamos obtener el número de lote
        gasto = GastosManoObra.objects.get(id=gasto_id) 
        lote = gasto.lote
        # Con el número de lote buscamos los salarios que vamos a eliminar
        salarios_a_eliminar = Salario.objects.filter(lote=lote)

        if salarios_a_eliminar.exists():
            num_eliminados = salarios_a_eliminar.count()
            salarios_a_eliminar.delete()
            # Mostrar un mensaje de éxito con el número de instancias eliminadas
            messages.success(request, f'Se han eliminado {num_eliminados} salarios del lote {lote} exitosamente.')
        else:
            # Mostrar un mensaje si no hay salarios asociados a ese lote
            messages.error(request, f'No se encontraron salarios asociados al lote {lote}.')

        return eliminar_operaciones_generico(
            request=request,
            slug=slug,
            modelo=GastosManoObra,
            instancia_id=gasto_id,
            redirect_url='contabilidad:gastos_mano_obra',  # URL a la que redirigir
        )
    
    else:
        # Mostrar un mensaje de advertencia
        messages.error(request, 'No se pueden hacer cambios a un proyecto inactivo.')
        # Redirigir a página de error
        return redirect('contabilidad:gastos_mano_obra',slug=slug)
    
@login_required
def eliminar_gastos_generales(request, slug, gasto_id):
    return eliminar_operaciones_generico(
            request=request,
            slug=slug,
            modelo=GastosGenerales,
            instancia_id=gasto_id,
            redirect_url='contabilidad:gastos_generales',  # URL a la que redirigir
        )

@login_required
def eliminar_gastos_equipos(request, slug, gasto_id):
    return eliminar_operaciones_generico(
            request=request,
            slug=slug,
            modelo=GastosEquipos,
            instancia_id=gasto_id,
            redirect_url='contabilidad:gastos_equipos',  # URL a la que redirigir
        )

@login_required
def eliminar_gastos_materiales(request, slug, gasto_id):
    return eliminar_operaciones_generico(
            request=request,
            slug=slug,
            modelo=GastosMateriales,
            instancia_id=gasto_id, 
            redirect_url='contabilidad:gastos_materiales',  # URL a la que redirigir
        )

@login_required
def eliminar_gastos_seguridad(request, slug, gasto_id):
    return eliminar_operaciones_generico(
            request=request,
            slug=slug,
            modelo=GastosSeguridad,
            instancia_id=gasto_id, 
            redirect_url='contabilidad:gastos_seguridad',  # URL a la que redirigir
        )

@login_required
def eliminar_gastos_vehiculos(request, slug, gasto_id):
    return eliminar_operaciones_generico(
            request=request,
            slug=slug,
            modelo=GastosVehiculos,
            instancia_id=gasto_id,  
            redirect_url='contabilidad:gastos_vehiculos',  # URL a la que redirigir
        )

@login_required
def eliminar_ingresos(request, slug, gasto_id):
    return eliminar_operaciones_generico(
            request=request,
            slug=slug,
            modelo=Ingresos,
            instancia_id=gasto_id, 
            redirect_url='contabilidad:ingresos',  # URL a la que redirigir
        )