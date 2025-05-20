from django import forms
from .models import Order
from django.utils.timezone import now


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'delivery_date',
            'departure_time',
            'arrival_time',
            'delivery_completed',
            'driver',
            'client',
            'status'
        ]
        labels = {
            'delivery_date': 'Data de Entrega',
            'departure_time': 'Data e hora de Saída',
            'arrival_time': 'Data e hora de chegada',
            'delivery_completed': 'Data e hora de conclusão',
            'driver': 'Motorista',
            'client': 'Cliente',
        }
        help_texts = {
            'client': 'Campo Obrigatório',
            'status': 'Campo Obrigatório',
            'delivery_date': 'Campo Obrigatório',
        }
        widgets = {
            'delivery_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'departure_time': forms.DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'arrival_time': forms.DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'delivery_completed': forms.DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'driver': forms.Select(attrs={'class': 'form-control'}),
            'client': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
        # Custom error messages
        error_messages = {
            'client': {
                'required': 'Campo obrigatório.',
            },
            'status': {
                'required': 'Campo obrigatório.',
            },
            'delivery_date': {
                'required': 'Campo obrigatório.',
            },
        }

    def clean(self):
        cleaned_data = super().clean()

        delivery_date = cleaned_data.get('delivery_date')
        departure_time = cleaned_data.get('departure_time')
        arrival_time = cleaned_data.get('arrival_time')
        delivery_completed = cleaned_data.get('delivery_completed')
        client = cleaned_data.get('client')
        status = cleaned_data.get('status')
        driver = cleaned_data.get('driver')

        # Data de entrega não pode ser no passado
        if delivery_date and delivery_date < now().date():
            self.add_error('delivery_date',
                           "A data de entrega não pode ser anterior a atual.")

        # Se status é diferente de 'pendente' precisa de motorista
        if status != 'pendente' and not driver:
            self.add_error('driver', "O motorista é obrigatório.")

        # Data de saída não pode ser anterior á data de entrega
        if departure_time and departure_time.date() < delivery_date:
            self.add_error('departure_time',
                           "A data e hora de saída não pode ser anterior a data de entrega.")
        # Data de chegada não pode ser anterior á data de entrega
        if arrival_time and arrival_time.date() < delivery_date:
            self.add_error('arrival_time',
                           "A data e hora de chegada não pode ser anterior a data de entrega.")
        # Data de conclusão não pode ser anterior á data de entrega
        if delivery_completed and delivery_completed.date() < delivery_date:
            self.add_error('delivery_completed',
                           "A data e hora de conclusão não pode ser anterior a data de entrega.")
        # Data de chegada não pode ser anterior á data de saída
        if arrival_time and departure_time and arrival_time < departure_time:
            self.add_error('arrival_time',
                           "A data e hora de chegada não pode ser anterior á data e hora de saída.")
        # Data de conclusão não pode ser anterior á data de saída
        if delivery_completed and departure_time and delivery_completed < departure_time:
            self.add_error('delivery_completed',
                           "A data e hora de conclusão não pode ser anterior á data e hora de saída.")
        # Se data de chegada estiver preenchido, data de saida não pode estar vazio
        if arrival_time and not departure_time:
            self.add_error(
                'departure_time', "A data e hora de saída devem estar preenchidas antes de concluir a entrega.")

        # Se delivery_completed estiver preenchido, arrival_time não pode estar vazio
        if delivery_completed and not arrival_time:
            self.add_error(
                'arrival_time', "A data e hora de chegada devem estar preenchidas antes de concluir a entrega.")

        # Data de conclusão não pode ser anterior á data de chegada
        if delivery_completed and arrival_time and delivery_completed < arrival_time:
            self.add_error('delivery_completed',
                           "A data e hora de conclusão não pode ser anterior á data e hora de chegada.")

        return cleaned_data
