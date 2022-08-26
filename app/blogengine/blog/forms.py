from django import forms
from .models import Tag, Post
from django.core.exceptions import ValidationError

class TagForm(forms.ModelForm):
    # title = forms.CharField(max_length=50)
    # slug = forms.CharField(max_length=50)
    #
    # title.widget.attrs.update({'class': 'form-control'})
    # slug.widget.attrs.update({'class': 'form-control'})
    class Meta:
        model = Tag
        fields = ['title', 'slug']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()

        if new_slug == 'create':
            raise ValidationError('Slug may not be "Create"')
        if Tag.objects.filter(slug__iexact=new_slug).count():
            raise ValidationError(f'Slug must be unique. We have "{new_slug}"')
        return new_slug


    # def save(self):
    #     new_tag = Tag.objects.create(title=self.cleaned_data['title'],
    #                                  slug=self.cleaned_data['slug'])
    #     return new_tag


class BondinsForm(forms.Form):
    inn = forms.CharField(max_length=50)

    inn.widget.attrs.update({'class': 'form-control'})
    def clean_inn(self):
        new_inn = self.cleaned_data['inn'].lower()


        if not new_inn.isdigit():
            raise ValidationError('Допустимы только цифры')
        elif len(new_inn) != 10:
            raise ValidationError('ИНН Должен содержать 10 цифр')
        return new_inn


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'body', 'tags']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()

        if new_slug == 'create':
            raise ValidationError('Slug may not be "Create"')
        # проверки на уникальность тут нет, так как хочется, чтобы слаг генерировался автоматически и проверялся в другом месте
        return new_slug
