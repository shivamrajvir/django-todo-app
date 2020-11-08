from django.forms import Form, ModelForm
from .models import Todo


class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'description', 'important']
