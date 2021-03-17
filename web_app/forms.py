from django import forms 
  
from .models import TestScore 
  
class TestScoreForm(forms.ModelForm): 
    class Meta: 
        model = TestScore 
        fields = "__all__"