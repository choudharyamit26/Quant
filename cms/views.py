from django.shortcuts import render
from django.views.generic import ListView
from .models import Post


class CMSView(ListView):
    model = Post
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        post = Post.objects.all()
        context = {
            'post': post
        }
        return render(self.request, "cms/index.html", context)

