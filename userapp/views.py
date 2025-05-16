from django.shortcuts import render, redirect
from userapp.forms import CustomUserForm,FileForm, ImageForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import Files,CustomUser,Images
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView, UpdateView
from django.http import HttpResponseForbidden
from django.core.mail import send_mail
from django.contrib import messages



# Create your views here.
def register_view(request):
    form = CustomUserForm()
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # Set password correctly
            user.save()
            return redirect('login')  # Redirect to login page after successful registration
    return render(request, 'userapp/register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('userfiles')  # Redirect to dashboard after successful login
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def userfiles(request):
    user = request.user
    search_query = request.GET.get('search', '')
    search_type = request.GET.get('search_type', 'all')

    # Filter files and images based on the search query and search_type
    user_files = Files.objects.filter(username=user)
    user_images = Images.objects.filter(username=user)

    if search_query:
        user_files = user_files.filter(file_name__icontains=search_query)
        user_images = user_images.filter(image_name__icontains=search_query)

    # Filter by type
    if search_type == 'file':
        user_images = []  # Hide images
    elif search_type == 'image':
        user_files = []   # Hide files

    # Initialize forms
    form = FileForm()
    image_form = ImageForm()

    if request.method == 'POST':
        # Handle image form submission
        if 'image_submit' in request.POST:
            image_form = ImageForm(request.POST, request.FILES)
            if image_form.is_valid():
                try:
                    image_instance = image_form.save(commit=False)
                    image_instance.username = user
                    image_instance.save()
                    return redirect('userfiles')
                except Exception as e:
                    print(f"Error saving image: {e}")
                    image_form.add_error(None, "An error occurred while saving the image.")

        # Handle file form submission
        elif 'file_submit' in request.POST:
            form = FileForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    file_instance = form.save(commit=False)
                    file_instance.username = user
                    file_instance.save()
                    return redirect('userfiles')
                except Exception as e:
                    print(f"Error saving file: {e}")
                    form.add_error(None, "An error occurred while saving the file.")

    context = {
        'image_form': image_form,
        'form': form,
        'post': user,
        'file': user_files,
        'images': user_images,
    }
    return render(request, 'userapp/userFiles.html', context)

def logout_handler(request):
    logout(request)
    return redirect('/home')


def dashboard(request):
    return render(request,'userapp/dashboard.html')


class FileDeleteView(DeleteView):
    model = Files
    template_name = 'userapp/confirm_delete.html'  # Optional: Create a confirmation template
    success_url = reverse_lazy('userfiles')  # Redirect to the userfiles page after deletion

    def get_queryset(self):
        # Ensure that only the logged-in user's files can be deleted
        return Files.objects.filter(username=self.request.user)

    def delete(self, request, *args, **kwargs):
        # Optional: Add custom logic before deletion
        file_instance = self.get_object()
        if file_instance.username != request.user:
            return HttpResponseForbidden("You are not allowed to delete this file.")
        return super().delete(request, *args, **kwargs)
    
class userUpdate(UpdateView):
    model = CustomUser
    template_name = 'userapp/user_update.html'  # Template for updating user information
    fields = ['username', 'first_name', 'last_name', 'address', 'contact', 'email']  # Fields to be updated
    success_url = reverse_lazy('userfiles')  # Redirect to the userfiles page after update

    def get_object(self, queryset=None):
        # Ensure that only the logged-in user's information can be updated
        return CustomUser.objects.get(pk=self.request.user.pk)
    
class ImageDeleteView(DeleteView):
    model = Images
    template_name = 'userapp/confirm_delete_image.html'  # Optional: Create a confirmation template
    success_url = reverse_lazy('userfiles')  # Redirect to the userfiles page after deletion

    def get_queryset(self):
        # Ensure that only the logged-in user's images can be deleted
        return Images.objects.filter(username=self.request.user)

    def delete(self, request, *args, **kwargs):
        # Optional: Add custom logic before deletion
        image_instance = self.get_object()
        if image_instance.username != request.user:
            return HttpResponseForbidden("You are not allowed to delete this image.")
        return super().delete(request, *args, **kwargs)
    

@login_required
def share_file(request):
    if request.method == 'POST':
        sender_email = request.POST.get('sender_email')
        receiver_email = request.POST.get('receiver_email')
        file_id = request.POST.get('file_id')

        try:
            file_instance = Files.objects.get(id=file_id, username=request.user)
            file_url = request.build_absolute_uri(file_instance.file.url)

            # Send email
            subject = f"File Shared by {sender_email}"
            message = f"Hello,\n\n{sender_email} has shared a file with you.\n\nFile Name: {file_instance.file_name}\nDownload Link: {file_url}\n\nBest regards,\nFile Clouding Team"
            send_mail(subject, message, sender_email, [receiver_email])

            messages.success(request, "File shared successfully!")
        except Files.DoesNotExist:
            messages.error(request, "File not found or you do not have permission to share it.")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

    return redirect('userfiles')

  