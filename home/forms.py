from django.forms import ModelForm
from .models import Profile, Product, Material
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    usable_password = None

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username']

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name']
    
class ProductForm(ModelForm):
    # category = forms.CharField(required=True)
    # supplier = forms.CharField(required=True)
    # colour = forms.CharField(required=True)

    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['user', 'picture', 'materials'] # , 'category'

class MaterialForm(ModelForm):
    class Meta:
        model = Material
        fields = '__all__'
        exclude = ['user', 'picture']