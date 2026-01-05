from django import forms
from .models import Thread

class ThreadCreateForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ["title"]
        widgets = {
            "title": forms.TextInput(attrs={
                "placeholder": "スレタイを入力（例：ｷﾀ━━━━(ﾟ∀ﾟ)━━━━!!）",
                "maxlength": 200,
            })
        }
