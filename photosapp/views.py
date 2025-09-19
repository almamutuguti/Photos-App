from django.shortcuts import render
from django.views.generic import ListView
from .models import Photo

# Create your views here.

def index(request):
    return render(request, 'index.html')

class PhotoListView(ListView):
    model = Photo
    template_name = 'photo_list.html'
    context_object_name = 'photos'
    paginate_by = 10 

