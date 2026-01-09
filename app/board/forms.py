from django import forms
from .models import Thread, Post

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

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["name", "email", "body"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "名前（例：名無しさん / nori#pass）"}),
            "email": forms.TextInput(attrs={"placeholder": "メール（sageで上げない）"}),
            "body": forms.Textarea(attrs={"rows": 5, "placeholder": "本文"}),
        }

    def clean_body(self):
        body = self.cleaned_data["body"].strip()
        if not body:
            raise forms.ValidationError("本文が空です")
        # 超簡易NGワード例（好きに増やしてOK）
        ng_words = ["死ね", "殺す"]  # ※強すぎるなら外す
        for w in ng_words:
            if w in body:
                raise forms.ValidationError("NGワードが含まれています")
        return body
