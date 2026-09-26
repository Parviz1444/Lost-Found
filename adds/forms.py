from django import forms
from .models import Post


class PostForm(forms.ModelForm):
   class Meta:
       model = Post
       fields = ["title", "content", "image"]

   def clean_image(self):
       image = self.cleaned_data.get("image")
       if image and image.size > 4 * 1024 * 1024:
           raise forms.ValidationError("Image files must be 4 MB or smaller.")
       return image
