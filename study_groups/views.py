from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import StudyGroup, Message, SharedFile, Notification, UserProfile 
from .forms import MessageForm, FileUploadForm
from django.contrib.auth.models import User
from .models import StudyGroup, Course

# Login Page
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully.')
            return redirect('dashboard')  # Redirect to dashboard
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login_page')

    return render(request, 'study_groups/login.html')


# Registration Page
def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register_page')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register_page')

        User.objects.create_user(username=username, password=password)
        messages.success(request, 'Registration successful! Please log in.')
        return redirect('login_page')

    return render(request, 'study_groups/register.html')


# Logout View
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login_page')


@login_required
def dashboard(request):
    notifications = Notification.objects.filter(user=request.user, read=False)
    return render(request, 'study_groups/dashboard.html', {'user': request.user, 'notifications': notifications})


# Join or Create Study Group Page
@login_required
def join_or_create_group(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        course_name = request.POST.get('course_name')
        description = request.POST.get('description')

        # Ensure the course is created or fetched correctly
        course, created = Course.objects.get_or_create(name=course_name)

        # Create the StudyGroup instance
        StudyGroup.objects.create(name=name, course=course, schedule=description)

        messages.success(request, 'Study group created successfully!')
        return redirect('join_or_create_group')

    groups = StudyGroup.objects.all()
    return render(request, 'study_groups/join_or_create.html', {'groups': groups})


@login_required
def view_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Update the user profile with the submitted data
        user_profile.preferred_study_times = request.POST.get('preferred_study_times', '')
        user_profile.learning_style = request.POST.get('learning_style', '')
        user_profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('view_profile')  # Redirect to the profile page after updating

    return render(request, 'study_groups/profile.html', {
        'user': request.user,
        'user_profile': user_profile,
    })


@login_required
def group_chat(request, group_id):
    group = get_object_or_404(StudyGroup, id=group_id)
    messages = group.messages.order_by('-timestamp')[:50]  # Show last 50 messages
    shared_files = group.shared_files.order_by('-timestamp')
    member_count = group.member_count()

    if request.method == 'POST':
        if 'message' in request.POST:
            form = MessageForm(request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.user = request.user
                message.group = group
                message.save()
                return redirect('group_chat', group_id=group.id)
        elif 'file' in request.FILES:
            file_form = FileUploadForm(request.POST, request.FILES)
            if file_form.is_valid():
                shared_file = file_form.save(commit=False)
                shared_file.user = request.user
                shared_file.group = group
                shared_file.save()
                return redirect('group_chat', group_id=group.id)

    form = MessageForm()
    file_form = FileUploadForm()

    return render(request, 'study_groups/groupchat.html', {  # Update this line
        'group': group,
        'messages': messages,
        'shared_files': shared_files,
        'form': form,
        'file_form': file_form,
        'member_count': member_count,
        'members': group.members.all(),
    })

@login_required
def search_groups(request):
    query = request.GET.get('q')
    if query:
        groups = StudyGroup.objects.filter(name__icontains=query)
    else:
        groups = StudyGroup.objects.all()
    return render(request, 'study_groups/search.html', {'groups': groups, 'query': query})