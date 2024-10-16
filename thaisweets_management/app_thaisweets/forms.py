from django import forms
from app_thaisweets.models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class SignupModelForm(UserCreationForm):
    class Meta(UserCreationForm.Meta): 
        # UserCreationForm = ใช้สร้างuserใหม่โดยจะมีแค่ username, password1, และ password2 
        fields = UserCreationForm.Meta.fields + ('email', 'first_name' , 'last_name')
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter your last name'}),
            'username': forms.TextInput(attrs={'placeholder': 'Enter your username'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
        }
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # exists() = ข้อมูลที่ทำการเช็คมีอยุ่แล้ว ถ้า Tมี จะerror 
        if User.objects.filter(email=email).exists(): 
            raise ValidationError("This email is already registered.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        username = cleaned_data.get('username')

        if User.objects.filter(email=email) and User.objects.filter(username=username).exists():
            self.add_error('username', "This username is already taken.")
        return cleaned_data
    
class SigninModelForm(forms.ModelForm):
    class Meta: 
        model = User
        fields = ['username', 'password']
        labels = {
            'username': 'Username',
            'password': 'Password',
        }
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter your username'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if username and password:
            # Authenticate = ตรวจสอบว่าข้อมูลที่ส่งเข้ามาตรงกับผู้ใช้ในระบบหรือไม่
            user = authenticate(username=username, password=password)

            if user is None:
                # ไม่มี user นี้หรืออาจจะกรอกข้อมูลผิด
                raise ValidationError("Invalid username or password")

        return cleaned_data
    

# ! for edit profile
class ProfileModelForm(forms.ModelForm):
    class Meta: 
        model = User
        fields = ['first_name','last_name']
        labels = {
            'first_name': 'Firstname',
            'last_name': 'Lastname',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter your last name'}),
        }
    
class ExtendProfileForm(forms.ModelForm):
    class Meta:
        model = Userprofile
        fields = ['age', 'image']
        labels = {
            'age': 'Age',
            'image': 'Image',
        }
        widgets = {
            'age': forms.TextInput(attrs={'placeholder': 'Enter your last name'}),
            'image': forms.FileInput(attrs={'accept': 'image/*'}),
        }

class PostModelForm(forms.ModelForm):
    Category  = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        required = True,
    )

    class Meta: 
        model = Post
        fields = ['title', 'body','Category', 'image']
        labels = {
            'title': 'Title',
            'body': 'Content', 
            'image':  'Image',
        }

        widgets = {
            'image': forms.FileInput(attrs={'accept': 'image/*'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        Category = cleaned_data.get('Category')
        if not Category:
                self.add_error('Category', 'Please select at least one category.')
        return cleaned_data
    
# class ExtendPostForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = ['image']
#         labels = {
#             'image': 'Image',
#         }
#         widgets = {
#             'image': forms.FileInput(attrs={'accept': 'image/*'}),
#         }
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Add a comment...'}),
        }