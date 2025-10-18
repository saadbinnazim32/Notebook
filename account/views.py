from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Message

def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        User.objects.create_user(username=name, email=email, password=password)
        return redirect('login')
    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')       # safer: use get()
        password = request.POST.get('password')

        user = authenticate(username=name, password=password)

        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_panel')
            else:
                return redirect('notes')
        else:
            # Invalid login, show error
            return render(request, 'login.html', {'error': 'Invalid username or password!'})

    return render(request, 'login.html')



@login_required
def notes(request):
    if request.method == 'POST':
        text = request.POST.get('note')  # note is the name her for text area in html file
        if text:
            Message.objects.create(user=request.user, text=text)
            return redirect('notes')
    notes = Message.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notes.html', {'notes': notes})


def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_panel(request):
    query = request.GET.get('q')  # get the search query from URL

    if query:
        all_messages = Message.objects.filter(user__username__icontains=query).order_by('-created_at')
    else:
        all_messages = Message.objects.all().order_by('-created_at')

    context = {
        'all_messages': all_messages,
        'query': query or ''
    }
    return render(request, 'admin_panel.html', context)




# @login_required
# def dashboard(request):
#     # Add message
#     if request.method == 'POST':
#         text = request.POST['message']
#         Message.objects.create(user=request.user, text=text)
#         return redirect('dashboard')

#     # Show only user's own messages
#     user_messages = Message.objects.filter(user=request.user)
#     return render(request, 'dashboard.html', {'messages': user_messages})