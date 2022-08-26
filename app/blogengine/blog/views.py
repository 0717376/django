from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import View
from django.core.exceptions import ValidationError

import json
import requests

from .models import Post, Tag
from .utils import *
from .forms import TagForm, BondinsForm, PostForm

def posts_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/index.html', context={'posts': posts})


class PostDetail(ObjectDetailMixin, View):
    model = Post
    template = 'blog/post_detail.html'
    # def get(self, request, slug):
    #     # post = Post.objects.get(slug__iexact=slug) - это то, как было ранее. Ниже новое через get_object
    #     post = get_object_or_404(Post, slug__iexact=slug)
    #     return render(request, 'blog/post_detail.html/', context={'post': post})

class PostCreate(CreateMixin, View):
    create_form = PostForm
    template = 'blog/post_create_form.html'

    # def get(self, request):
    #     form = PostForm()
    #     return render(request, 'blog/post_create_form.html', context={'form': form})
    #
    # def post(self, request):
    #     bound_form = PostForm(request.POST)
    #
    #     if bound_form.is_valid():
    #         new_post = bound_form.save()
    #         return redirect(new_post)
    #     return render(request, 'blog/post_create_form.html', context={'form': bound_form})

class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'blog/tag_detail.html'
    # def get(self, request, slug):
    #     tag = get_object_or_404(Tag, slug__iexact=slug)
    #     return render(request, 'blog/tag_detail.html', context={'tag': tag})


class TagCreate(CreateMixin, View):
    create_form = TagForm
    template = 'blog/tag_create.html'



def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tags_list.html', context={'tags': tags})


class Bondins(View):
    def get(self, request):
        form = BondinsForm
        return render(request, 'blog/bondins.html', context={'form': form})

    def post(self, request):
        bound_form = BondinsForm(request.POST)
        if bound_form.is_valid():
            response = requests.get(f"https://focus-api.kontur.ru/api3/briefReport?inn={bound_form.cleaned_data['inn']}&key=ZFEmineQeAa7ZmJhvbPQNs1HWuxp7D9gDKyRWmVp")
            todos = json.loads(response.text)
            try:
                link = todos[0]['briefReport']['href']
            except IndexError:
                bound_form.add_error('inn', 'нет такого ИНН')
                return render(request, 'blog/bondins.html', context={'form': bound_form})
            return redirect(link)
        return render(request, 'blog/bondins.html', context={'form': bound_form})
