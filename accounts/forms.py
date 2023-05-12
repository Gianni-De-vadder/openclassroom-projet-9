from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class SignupForm(UserCreationForm):
    """Fields for signup page"""

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username", "email", "password1", "password2")

        error_messages = {
            "password_mismatch": "Les mots de passe ne correspondent pas.",
            "password_too_short": "Le mot de passe doit contenir au moins %(min_length)d caractères.",
            "password_common": "Le mot de passe ne peut pas être un mot de passe couramment utilisé.",
            "password_entirely_numeric": "Le mot de passe ne peut pas être entièrement numérique.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[
            "username"
        ].help_text = ""  # Supprime le message d'erreur pour le champ username
