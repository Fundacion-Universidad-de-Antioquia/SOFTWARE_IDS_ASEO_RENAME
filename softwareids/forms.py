from django import forms
from .models import  Usuario, Campo, NovedadBase
from datetime import date
from django.forms import DateInput, TextInput, Select, TimeInput
from .utils import fetch_zonas_from_odoo, fetch_personas_from_odoo, fetch_rutas_from_odoo,fetch_personas_from_odoo_usuarios

class NovedadFormBase(forms.Form):
    #fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date','readonly': 'readonly'}))
    fecha = forms.DateField(widget=TextInput(attrs={'readonly': 'readonly','type': 'date', 'class': 'form-control'}))
    justificacion = forms.CharField(widget=forms.HiddenInput(), required=False)  # Ocultar el campo con CSS
    #fecha = forms.DateField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    #fecha = forms.DateField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), initial=date.today)
    Persona = forms.ChoiceField(choices=[], label='Persona')
    zona = forms.ChoiceField(choices=[], label='Zona')
    novedad_extemporanea = forms.ChoiceField(
        widget=Select(attrs={'class': 'form-control'}),
        choices=[
            ('opcion1', 'Si'),
            ('opcion2', 'No'),
        ],
        label='Novedad Extemporánea',
        initial='opcion2'  # Establecer valor predeterminado a "No"
    )

    def __init__(self, *args, **kwargs):
        departamento = kwargs.pop('departamento', None) 
        initial = kwargs.get('initial', {})
        initial.setdefault('fecha', date.today().isoformat())  # Establecer la fecha predeterminada
        kwargs['initial'] = initial
        super().__init__(*args, **kwargs)
        
        zonas = fetch_zonas_from_odoo()
        zona_choices = [(zona, zona) for zona in zonas]
        personas = fetch_personas_from_odoo(departamento)
        persona_choices = [(persona[0], f"{persona[0]} - {persona[1]}") for persona in personas]
        self.fields['zona'].choices = zona_choices
        self.fields['Persona'].choices = persona_choices
        self.personas_data = {persona[0]: persona for persona in personas}  # Almacena los datos de las personas
        

    def get_persona_data(self, identification_id):
        return self.personas_data.get(identification_id)
class NovedadFormTipo1(NovedadFormBase, forms.ModelForm):
    class Meta:
        model = Campo
        fields = ['novedad_extemporanea','fecha','Persona','zona','observaciones']
        widgets = {
            'observaciones': TextInput(attrs={'class': 'form-control'})
        }

class NovedadFormTipo2(NovedadFormBase, forms.ModelForm):
    class Meta:
        model = Campo
        fields = ['novedad_extemporanea','fecha','Persona','zona','tipo_permisos','observaciones']
        widgets = {
            'tipo_permisos': Select(attrs={'class': 'form-control'}),
            'observaciones': TextInput(attrs={'class': 'form-control'})
        }
class NovedadFormTipo3(NovedadFormBase, forms.ModelForm):
    colaborador = forms.ChoiceField(choices=[], label='Colaborador Reemplazo')
    rutas = forms.ChoiceField(choices=[], label='Ruta')
    zona_reemplazo = forms.ChoiceField(choices=[], label='Zona Reemplazo')
    cantidad_horas = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}), required=False, label='Cantidad de Horas')

    class Meta:
        model = Campo
        fields = ['novedad_extemporanea','fecha','Persona','zona','rutas', 'reemplaza', 'colaborador','zona_reemplazo', 'horasextra', 'hora_inicio', 'hora_fin', 'cantidad_horas']
        widgets = {
            'reemplaza': Select(attrs={'class': 'form-control'}),
            'horasextra': Select(attrs={'class': 'form-control'}),
            'rutas': Select(attrs={'class': 'form-control'}),
            'hora_inicio': TimeInput(attrs={'class': 'form-control', 'type': 'time'}),  # Widget de tiempo
            'hora_fin': TimeInput(attrs={'class': 'form-control', 'type': 'time'})  # Widget de tiempo
        }
    def __init__(self, *args, **kwargs):
        departamento = kwargs.pop('departamento', None) 
        super().__init__(*args, **kwargs)
        self.fields['hora_inicio'].required = False
        self.fields['hora_fin'].required = False
        
        rutas = fetch_rutas_from_odoo()
        ruta_choices = [(ruta, ruta) for ruta in rutas]
        self.fields['rutas'].choices = ruta_choices
        self.fields['rutas'].widget.attrs.update({'class': 'form-control'})  # Añadir la clase 'form-control'
        

        zonas = fetch_zonas_from_odoo()
        zona_choices = [(zona, zona) for zona in zonas]
        self.fields['zona_reemplazo'].choices = zona_choices
        self.fields['zona_reemplazo'].widget.attrs.update({'class': 'form-control'})  # Añadir la clase 'form-control'


        personas = fetch_personas_from_odoo(departamento)
        persona_choices = [(persona[0], f"{persona[0]} - {persona[1]}") for persona in personas]
        self.fields['Persona'].choices = persona_choices
        
        # Aquí, colaborador_choices se puede inicializar igual que persona_choices 
        # ya que se está filtrando por el mismo departamento.
        colaborador_choices = persona_choices
        self.fields['colaborador'].choices = colaborador_choices

class TiposNovedades(forms.ModelForm):
    class Meta:
        model = NovedadBase
        fields = ['tipo_novedad']

        

class NovedadFormTipo4(NovedadFormBase, forms.ModelForm):
    zona_reemplazo = forms.ChoiceField(choices=[], label='Zona Reemplazo')
    colaborador = forms.ChoiceField(choices=[], label='Colaborador Reemplazo')
    zona_inicial = forms.ChoiceField(choices=[], label='Zona Inicial')
    class Meta:
        model = Campo
        fields = ['novedad_extemporanea','fecha','Persona','zona','reemplaza']
        widgets = {
            'reemplaza': Select(attrs={'class': 'form-control'})
        
        }
    def __init__(self, *args, **kwargs):
        
        departamento = kwargs.pop('departamento', None) 
        super().__init__(*args, **kwargs)
        zona_inicial = fetch_zonas_from_odoo()
        zona_choices = [(zona, zona) for zona in zona_inicial]
        self.fields['zona_inicial'].choices = zona_choices
        self.fields['zona_inicial'].widget.attrs.update({'class': 'form-control'})  # Añadir la clase 'form-control'
        
        personas = fetch_personas_from_odoo(departamento)
        persona_choices = [(persona[0], f"{persona[0]} - {persona[1]}") for persona in personas]
        self.fields['Persona'].choices = persona_choices
        
        # Aquí, colaborador_choices se puede inicializar igual que persona_choices 
        # ya que se está filtrando por el mismo departamento.
        colaborador_choices = persona_choices
        self.fields['colaborador'].choices = colaborador_choices
        
        zona_reemplazo = fetch_zonas_from_odoo()
        zona_choices = [(zona, zona) for zona in zona_reemplazo]
        self.fields['zona_reemplazo'].choices = zona_choices  
        self.fields['zona_reemplazo'].widget.attrs.update({'class': 'form-control'})  # Añadir la clase 'form-control'
        
         

class NovedadFormTipo5(NovedadFormBase, forms.ModelForm):
    class Meta:
        model = Campo
        fields = ['novedad_extemporanea','fecha','Persona','zona','hora_llegada']
        widgets = {
            'hora_llegada': TimeInput(attrs={'class': 'form-control', 'type': 'time'}),       
        }

class NovedadFormTipo6(NovedadFormBase, forms.ModelForm):
    
    cantidad_horas = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}), required=False, label='Cantidad de Horas')
    class Meta:
        model = Campo
        fields = ['novedad_extemporanea','fecha','Persona','zona','horasextra','hora_inicio', 'hora_fin','cantidad_horas','observaciones']
        widgets = {
            'horasextra': Select(attrs={'class': 'form-control'}),
            'hora_inicio': TimeInput(attrs={'class': 'form-control', 'type': 'time'}),  # Widget de tiempo
            'hora_fin': TimeInput(attrs={'class': 'form-control', 'type': 'time'}),    # Widget de tiempo
            'observaciones': TextInput(attrs={'class': 'form-control'})
        
        }
class NovedadFormTipo7(NovedadFormBase, forms.ModelForm):
    zona_reemplazo = forms.ChoiceField(choices=[], label='Zona Reemplazo')
    rutas = forms.ChoiceField(choices=[], label='Ruta')
    colaborador = forms.ChoiceField(choices=[], label='Colaborador Reemplazo')
    cantidad_horas = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}), required=False, label='Cantidad de Horas')
    class Meta:
        model = Campo
        fields = ['novedad_extemporanea','fecha','tipo_incapacidad','Persona','zona','rutas', 'reemplaza','colaborador','zona_reemplazo','horasextra','hora_inicio', 'hora_fin','cantidad_horas', 'observaciones']
        widgets = {
            'reemplaza': Select(attrs={'class': 'form-control'}),
            'tipo_incapacidad': Select(attrs={'class': 'form-control'}),
            'observaciones': TextInput(attrs={'class': 'form-control'}),
            'horasextra': Select(attrs={'class': 'form-control'}),
            'cantidad_horas': Select(attrs={'class': 'form-control'}),
            'hora_inicio': TimeInput(attrs={'class': 'form-control', 'type': 'time'}),  # Widget de tiempo
            'hora_fin': TimeInput(attrs={'class': 'form-control', 'type': 'time'})    # Widget de tiempo
        
        }
    def __init__(self, *args, **kwargs):
        
        departamento = kwargs.pop('departamento', None) 
        super().__init__(*args, **kwargs)
        zona_reemplazo = fetch_zonas_from_odoo()
        zona_choices = [(zona, zona) for zona in zona_reemplazo]
        self.fields['zona_reemplazo'].choices = zona_choices 
        self.fields['zona_reemplazo'].widget.attrs.update({'class': 'form-control'})  # Añadir la clase 'form-control'  
        
        rutas = fetch_rutas_from_odoo()
        ruta_choices = [(ruta, ruta) for ruta in rutas]
        self.fields['rutas'].choices = ruta_choices
        self.fields['rutas'].widget.attrs.update({'class': 'form-control'})  # Añadir la clase 'form-control'
        
        personas = fetch_personas_from_odoo(departamento)
        persona_choices = [(persona[0], f"{persona[0]} - {persona[1]}") for persona in personas]
        self.fields['Persona'].choices = persona_choices
        
        # Aquí, colaborador_choices se puede inicializar igual que persona_choices 
        # ya que se está filtrando por el mismo departamento.
        colaborador_choices = persona_choices
        self.fields['colaborador'].choices = colaborador_choices
        
    
         

class NovedadFormTipo8(NovedadFormBase, forms.ModelForm):
    fecha_ingreso = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}), required=False, label='Fecha de Ingreso')

    class Meta:
        model = Campo
        fields = ['novedad_extemporanea','fecha','Persona','zona','fecha_ingreso']  # Añadir los campos necesarios

    def __init__(self, *args, **kwargs):
        super(NovedadFormTipo8, self).__init__(*args, **kwargs)
        self.fields['fecha_ingreso'].widget.attrs['readonly'] = True


class DateInput(forms.DateInput):
    input_type = 'date'

class NovedadFormTipo9(NovedadFormBase, forms.ModelForm):
    cantidad_dias = forms.IntegerField(
    widget=forms.NumberInput(attrs={'class': 'form-control'}),  # Usa NumberInput para los campos numéricos
    label='Cantidad de Días',
    required=False
    )   
    class Meta:
        model = Campo
        fields = ['novedad_extemporanea','fecha', 'tipos_licencia','Persona','zona','fecha_inicial', 'fecha_final']
        widgets = {
            'fecha_inicial': DateInput(attrs={'class': 'form-control'}),
            'fecha_final': DateInput(attrs={'class': 'form-control'}),
            'tipos_licencia': Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cantidad_dias'].widget.attrs['readonly'] = True


class NovedadFormTipo10(NovedadFormBase, forms.ModelForm):
    class Meta:
        model = Campo
        fields = ['novedad_extemporanea','fecha','Persona','zona','observaciones']        
        widgets = {
            'observaciones': TextInput(attrs={'class': 'form-control'})
        }

class NovedadFormTipo11(NovedadFormBase, forms.ModelForm):
    
    cantidad_dias = forms.IntegerField(
    widget=forms.NumberInput(attrs={'class': 'form-control'}),  # Usa NumberInput para los campos numéricos
    label='Cantidad de Días',
    required=False
    )
    class Meta:
        model = Campo
        fields = ['novedad_extemporanea','fecha','Persona','zona','fecha_inicial', 'fecha_final']
        widgets = {
            'fecha_inicial': DateInput(attrs={'class': 'form-control'}),
            'fecha_final': DateInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cantidad_dias'].widget.attrs['readonly'] = True

class NovedadFormTipo12(NovedadFormBase, forms.ModelForm):
    class Meta:
        model = Campo
        fields = ['novedad_extemporanea','fecha','Persona','zona','observaciones']
        widgets = {
            'observaciones': TextInput(attrs={'class': 'form-control'})
        }

class NovedadFormTipo13(NovedadFormBase, forms.ModelForm):
    class Meta:
        model = Campo
        fields = ['novedad_extemporanea','fecha','Persona','zona','observaciones']
        widgets = {
            'observaciones': TextInput(attrs={'class': 'form-control'})
        }
class NovedadFormTipo14(NovedadFormBase, forms.ModelForm):
    class Meta:
        model = Campo
        fields = ['novedad_extemporanea','fecha','Persona','zona','observaciones']
        widgets = {
            'observaciones': TextInput(attrs={'class': 'form-control'})
        }

class NovedadFormTipo15(NovedadFormBase, forms.ModelForm):
    class Meta:
        model = Campo
        fields = ['novedad_extemporanea','fecha','Persona','zona','observaciones']
        widgets = {
            'observaciones': TextInput(attrs={'class': 'form-control'})
        }

class NovedadFormTipo16(NovedadFormBase, forms.ModelForm):
    zona_inicial = forms.ChoiceField(choices=[], label='Zona Inicial')
    colaborador = forms.ChoiceField(choices=[], label='Recolector 1')
    colaborador2 = forms.ChoiceField(choices=[], label='Recolector 2')
    conductor = forms.ChoiceField(choices=[], label='Conductor')
    class Meta:
        model = Campo
        fields = ['novedad_extemporanea','fecha','Persona','colaborador2','conductor','control', 'nuevo_control']
        widgets = {
            'control': TextInput(attrs={'class': 'form-control'}),
            'nuevo_control': TextInput(attrs={'class': 'form-control'})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        departamento = kwargs.pop('departamento', None) 
        zonas = fetch_zonas_from_odoo()
        zona_choices = [(zona, zona) for zona in zonas]
        self.fields['zona_inicial'].choices = zona_choices    
        self.fields['zona_inicial'].widget.attrs.update({'class': 'form-control'})  # Añadir la clase 'form-control' 
        
        personas = fetch_personas_from_odoo(departamento)
        persona_choices = [(persona[0], f"{persona[0]} - {persona[1]}") for persona in personas]
        # Aquí, colaborador_choices se puede inicializar igual que persona_choices 
        # ya que se está filtrando por el mismo departamento.
        colaborador_choices = persona_choices
        self.fields['colaborador'].choices = colaborador_choices
        
        colaborador_choices2 = persona_choices
        self.fields['colaborador2'].choices = colaborador_choices2
        self.fields['colaborador2'].widget.attrs.update({'class': 'form-control'}) 
        
        conductor_choices = persona_choices
        self.fields['conductor'].choices = conductor_choices
        self.fields['conductor'].widget.attrs.update({'class': 'form-control'}) 

class NovedadFormTipo17(NovedadFormBase, forms.ModelForm):
    cantidad_dias = forms.IntegerField(
        label='Cantidad de Días', 
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )
    #cantidad_dias = forms.IntegerField(label='Cantidad de Días', required=False)
    class Meta:
        model = Campo
        fields = ['novedad_extemporanea','fecha','Persona','zona','fecha_inicial', 'fecha_final','cantidad_dias', 'observaciones']
        widgets = {
            'fecha_inicial': DateInput(attrs={'class': 'form-control'}),
            'fecha_final': DateInput(attrs={'class': 'form-control'}),
            'observaciones': TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cantidad_dias'].widget.attrs['readonly'] = True

class NovedadFormTipo18(NovedadFormBase, forms.ModelForm):
    class Meta:
        model = Campo
        fields = ['novedad_extemporanea','fecha','Persona','zona','motivo_renuncia']
        widgets = {
            'motivo_renuncia': TextInput(attrs={'class': 'form-control'})
        }

class NovedadFormTipo19(NovedadFormBase, forms.ModelForm):
    rutas = forms.ChoiceField(choices=[], label='Ruta')
    colaborador = forms.ChoiceField(choices=[], label='Recolector 1')
    colaborador2 = forms.ChoiceField(choices=[], label='Recolector 2')
    conductor = forms.ChoiceField(choices=[], label='Conductor')
    class Meta:
        model = Campo
        fields = ['novedad_extemporanea','fecha','Persona','colaborador2','conductor','zona','rutas','control', 'hora_salida', 'observaciones']
        widgets = {
            'hora_salida':TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'control': TextInput(attrs={'class': 'form-control'}),
            'observaciones': TextInput(attrs={'class': 'form-control'}) 
        }
    def __init__(self, *args, **kwargs):
        departamento = kwargs.pop('departamento', None) 
        super().__init__(*args, **kwargs)
        rutas = fetch_rutas_from_odoo()
        ruta_choices = [(ruta, ruta) for ruta in rutas]
        self.fields['rutas'].choices = ruta_choices
        self.fields['rutas'].widget.attrs.update({'class': 'form-control'}) 
        
        personas = fetch_personas_from_odoo(departamento)
        persona_choices = [(persona[0], f"{persona[0]} - {persona[1]}") for persona in personas]
        # Aquí, colaborador_choices se puede inicializar igual que persona_choices 
        # ya que se está filtrando por el mismo departamento.
        colaborador_choices = persona_choices
        self.fields['colaborador'].choices = colaborador_choices
        
        colaborador_choices2 = persona_choices
        self.fields['colaborador2'].choices = colaborador_choices2
        self.fields['colaborador2'].widget.attrs.update({'class': 'form-control'}) 
        
        conductor_choices = persona_choices
        self.fields['conductor'].choices = conductor_choices
        self.fields['conductor'].widget.attrs.update({'class': 'form-control'}) 

class NovedadFormTipo20(NovedadFormBase, forms.ModelForm):
    cantidad_horas = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'form-control'}), required=False, label='Cantidad de Horas')
    class Meta:
        model = Campo
        fields = ['novedad_extemporanea','fecha','Persona','zona','tipo_servicio','consecutivo','horasextra', 'hora_inicio', 'hora_fin', 'cantidad_horas']
        widgets = {
            'horasextra': Select(attrs={'class': 'form-control', 'type': 'time'}),  # Widget de tiempo
            'hora_inicio': TimeInput(attrs={'class': 'form-control', 'type': 'time'}),  # Widget de tiempo
            'hora_fin': TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }
        
class NovedadFormTipo21(NovedadFormBase, forms.ModelForm):
    rutas = forms.ChoiceField(choices=[], label='Ruta')   
    cantidad_horas = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}), required=False, label='Cantidad de Horas')
    colaborador = forms.ChoiceField(choices=[], label='Colaborador Reemplazo')
    rutas = forms.ChoiceField(choices=[], label='Ruta')
    class Meta:
        model = Campo
        fields = [ 'novedad_extemporanea','fecha','Persona','zona','rutas','horasextra','hora_inicio', 'hora_fin','cantidad_horas','reemplaza', 'colaborador','zona_reemplazo',]
        widgets = {
            'horasextra': Select(attrs={'class': 'form-control', 'type': 'time'}),  # Widget de tiempo
            'hora_inicio': TimeInput(attrs={'class': 'form-control', 'type': 'time'}),  # Widget de tiempo
            'hora_fin': TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'reemplaza': Select(attrs={'class': 'form-control', 'type': 'time'})
        }
    def __init__(self, *args, **kwargs):
        departamento = kwargs.pop('departamento', None) 
        super().__init__(*args, **kwargs)
        rutas = fetch_rutas_from_odoo()
        ruta_choices = [(ruta, ruta) for ruta in rutas]
        self.fields['rutas'].choices = ruta_choices   
        self.fields['rutas'].widget.attrs.update({'class': 'form-control'})     
       
        zonas = fetch_zonas_from_odoo()
        zona_choices = [(zona, zona) for zona in zonas]
        self.fields['zona_reemplazo'].choices = zona_choices
        self.fields['zona_reemplazo'].widget.attrs.update({'class': 'form-control'})  # Añadir la clase 'form-control'


        personas = fetch_personas_from_odoo(departamento)
        persona_choices = [(persona[0], f"{persona[0]} - {persona[1]}") for persona in personas]
        self.fields['Persona'].choices = persona_choices
        
        # Aquí, colaborador_choices se puede inicializar igual que persona_choices 
        # ya que se está filtrando por el mismo departamento.
        colaborador_choices = persona_choices
        self.fields['colaborador'].choices = colaborador_choices
   

class NovedadFormTipo22(NovedadFormBase, forms.ModelForm):
    rutas = forms.ChoiceField(choices=[], label='Ruta')   
    class Meta:
        model = Campo
        fields = ['novedad_extemporanea','fecha','Persona','zona','rutas','observaciones']  
        widgets = {
            'observaciones': TextInput(attrs={'class': 'form-control'})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        rutas = fetch_rutas_from_odoo()
        ruta_choices = [(ruta, ruta) for ruta in rutas]
        self.fields['rutas'].choices = ruta_choices     
        self.fields['rutas'].widget.attrs.update({'class': 'form-control'})     

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['cedula', 'nombre', 'correo','departamento']

class CampoForm(forms.ModelForm):
    fecha = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',  # Esto utiliza el selector de fecha HTML5
                'class': 'form-control',  # Clase CSS para Bootstrap
                'readonly': 'readonly',  # Bloquear el campo de fecha
                'placeholder': 'Seleccione una fecha'  # Texto de marcador de posición
            }
        ),
        input_formats=['%Y-%m-%d'],  # Formato de entrada esperado
    )

    zona = forms.ChoiceField(choices=[], label='Zona')

    justificacion = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',  # Asegurarse de que tenga la clase form-control para el estilo
                'placeholder': 'Justifique por qué no realizó el reporte del día anterior en el horario establecido',
                'rows': 3,
                'id': 'justificacion-textarea'  # Identificador único
            }
        ),
        required=False,
        label='Justificación'
    )

    class Meta:
        model = NovedadBase
        fields = ['fecha', 'zona', 'justificacion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Obtener las zonas desde Odoo
        zonas = fetch_zonas_from_odoo()
        zona_choices = [(zona, zona) for zona in zonas]
        self.fields['zona'].choices = zona_choices