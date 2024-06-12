from django.http.response import HttpResponse, Http404
from django.shortcuts import render
from django.template import loader
from blogging.models import Post
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

#class BlogStubView():
    #template_name = 


def stub_view(request, *args, **kwargs):
    body = "Stub View\n\n"
    if args:
        body += "Args: \n"
        body += "\n".join(["\t%s: %s" % i for i in args])
    if kwargs:
        body+= "Kwargs:\n"
        body+= "\n".join(["\t%s: %s" % i for i in kwargs.items()])
    return HttpResponse(body, content_type="text/plain")


def old_list_view(request):
    published = Post.objects.exclude(published_date__exact = None)
    posts = published.order_by('-published_date')
    template = loader.get_template('blogging/list.html')
    context = {'posts': posts}
    body = template.render(context)
    return HttpResponse(body, content_type="text/html")

class PostListView(ListView):
    model = Post
    template_name = 'blogging/list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.exclude(published_date__isnull=True).order_by('-published_date')

def list_view(request):
    published = Post.objects.exclude(published_date__exact=None)
    posts = published.order_by('-published_date')
    context = {'posts': posts}
    return render(request, 'blogging/list.html', context)

class PostDetailView(DetailView):
    model = Post
    template_name = 'blogging/detail.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.exclude(published_date__isnull=True)
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.published_date is None:
            raise Http404
        return obj

def detail_view(request, post_id):
    published = Post.objects.exclude(published_date__exact=None)
    try:
        post = published.get(pk=post_id)
    except Post.DoesNotExist:
        raise Http404
    context = {'post': post}
    return render(request, 'blogging/detail.html', context)
