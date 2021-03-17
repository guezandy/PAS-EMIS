from django import forms 
  
from web_app.models.main import TestScore 
  
class TestScoreForm(forms.ModelForm): 
    class Meta: 
        model = TestScore 
        fields = "__all__"