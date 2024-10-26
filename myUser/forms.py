# accounts/forms.py
from django import forms
from django.conf import settings
from .models import MyUser,Profile
from django.contrib.auth import get_user_model

from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm, UserCreationForm,AuthenticationForm

CustomUser = settings.AUTH_USER_MODEL

# pour se inscription

class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = MyUser
        fields = ("email","pseudo",)

# pour se modification
class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = MyUser
        fields = ("email","pseudo","user_image")

# pour se connecter
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email', max_length=254)

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']
        
# pour se changer mot de pass

class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = MyUser
        fields = ['old_password', 'new_password1', 'new_password2']
        
    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError("L'ancien mot de passe est incorrect.")
        return old_password     
    
    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("Les deux nouveaux mots de passe ne correspondent pas.")
        return new_password2
    


       
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture', 'facebook_link', 'linkedin_link', 'instagram_link']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'facebook_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Facebook URL'}),
            'linkedin_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'LinkedIn URL'}),  # Correction de l'espace
            'instagram_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Instagram URL'}),
        }