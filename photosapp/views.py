from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.contrib import messages
from .models import Photo, Tag, UserInteraction
from .forms import ProfileUpdateForm, PhotoUploadForm


# Create your views here.

def index(request):
    return render(request, 'index.html')

def home(request):
    photos = Photo.objects.all().select_related('uploaded_by').prefetch_related('tags')
    tags = Tag.objects.annotate(photo_count=Count('photo')).order_by('-photo_count')[:10]

    #get filter parameters
    tag_filter = request.GET.get('tag')
    if tag_filter:
        photos = photos.filter(tags__name=tag_filter)
    
    context = {
        'photos': photos,
        'tags': tags,
        'selected_tag': tag_filter,
    }

    return render(request, 'home.html', context)

def photo_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    user_interaction = None
    

    if request.user.is_authenticated:
        user_interaction, created = UserInteraction.objects.get_or_create(
            user=request.user,
            photo=photo
        )

    context = {
        'photo': photo,
        'user_interaction': user_interaction,
    }
    return render(request, 'photo_detail.html', context)

@login_required
def upload_photo(request):
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.uploaded_by = request.user
            photo.save()
            
            # Process tags
            tags_input = form.cleaned_data['tags']
            if tags_input:
                tags = [tag.strip() for tag in tags_input.split(',')]
                for tag_name in tags:
                    tag, created = Tag.objects.get_or_create(name=tag_name.lower())
                    photo.tags.add(tag)
            
            messages.success(request, 'Photo uploaded successfully!')
            return redirect('photo_detail', pk=photo.pk)
    else:
        form = PhotoUploadForm()
    
    return render(request, 'upload_photo.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(
            request.POST, 
            request.FILES, 
            instance=request.user.profile
        )
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    
    user_photos = Photo.objects.filter(uploaded_by=request.user)
    liked_photos = Photo.objects.filter(
        userinteraction__user=request.user,
        userinteraction__liked=True
    )
    
    context = {
        'form': form,
        'user_photos': user_photos,
        'liked_photos': liked_photos,
    }
    return render(request, 'profile.html', context)