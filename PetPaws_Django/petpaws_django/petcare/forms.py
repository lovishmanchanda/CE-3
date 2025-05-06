from django import forms
from .models import CareTip, Hospital, Food, Clothes, Medicine, Accessory

class CareTipForm(forms.ModelForm):
    class Meta:
        model = CareTip
        fields = ['title', 'description']

class HospitalForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = ['name', 'address', 'contact_number', 'emergency_available']

class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['name', 'brand', 'price', 'image']

class ClothesForm(forms.ModelForm):
    class Meta:
        model = Clothes
        fields = ['name', 'size', 'color', 'price', 'image']

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'usage', 'price', 'image']

class AccessoryForm(forms.ModelForm):
    class Meta:
        model = Accessory
        fields = ['name', 'type', 'price', 'image']
