from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from .models import MyUser as User
from django.core.validators import RegexValidator, MinLengthValidator


class UserCreationForm(forms.ModelForm):
    """Form for creating regular users and superusers."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["email", "username"]

    def clean_password2(self):
        """Check both passwords match"""
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")

        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match")
        return p2

    def save(self, commit=True):
        """Save hashed password"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """Form used in admin for updating users."""

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "password",
            "is_active",
            "is_admin",
            "is_staff",
            "is_superuser",
        ]


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={"placeholder": "Username", "class": "form-control"}
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control",
                "id": "password-field",
            }
        )
    )


class SignupForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Username"}
        ),
        validators=[
            MinLengthValidator(3),
            RegexValidator(
                regex=r"^[a-zA-Z0-9_]+$",
                message="Username can only contain letters, numbers, and underscores.",
            ),
        ],
    )
    email = forms.EmailField(
        max_length=50,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Email"}
        ),
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        ),
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm Password"}
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        errors = []

        # جمع تمام خطاهای فیلدها
        for field in self:
            for error in field.errors:
                errors.append(error)

        username = cleaned_data.get("username")
        email = cleaned_data.get("email")

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # خطاهای clean اصلی
        if password and confirm_password and password != confirm_password:
            errors.append("Password and Confirm Password do not match")

        if username and User.objects.filter(username=username).exists():
            errors.append("This username is already taken.")

        if email and User.objects.filter(email=email).exists():
            errors.append("This email is already registered.")

        if errors:
            raise forms.ValidationError(errors)

        return cleaned_data
