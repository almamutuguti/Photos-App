from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Photo, Tag, Like


# Create your views here.

def index(request):
    return render(request, 'index.html')

class PhotoListView(ListView):
    model = Photo
    template_name = 'photos/photo_list.html'
    context_object_name = 'photos'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-uploaded_at')
        tag_name = self.request.GET.get('tag')
        if tag_name:
            tag = get_object_or_404(Tag, name=tag_name)
            queryset = queryset.filter(tags=tag)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context

class PhotoDetailView(DetailView):
    model = Photo
    template_name = 'photos/photo_detail.html'
    context_object_name = 'photo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        photo = self.get_object()
        if self.request.user.is_authenticated:
            context['user_has_liked'] = Like.objects.filter(photo=photo, user=self.request.user).exists()
        return context

@login_required
def like_photo(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if not Like.objects.filter(photo=photo, user=request.user).exists():
        Like.objects.create(photo=photo, user=request.user)
    return redirect('photo_detail', pk=pk)

@login_required
def unlike_photo(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    Like.objects.filter(photo=photo, user=request.user).delete()
    return redirect('photo_detail', pk=pk)