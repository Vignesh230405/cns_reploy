from django.shortcuts import render, redirect
from users.models import MyUsers
from .models import Post
from .forms import PostForm
from .utils import encrypt_message, decrypt_message

def home(request):
    return render(request, "main/home.html")

def about(request):
    return render(request, "main/about.html")

def global_chat(request):
    username = request.session.get("username")
    if not username:
        return redirect("login")
    
    user = MyUsers.objects.get(username=username)
    
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            plaintext = form.cleaned_data["content"]
            ciphertext = encrypt_message(plaintext)

            Post.objects.create(
                sender=user,
                ciphertext=ciphertext
            )
            return redirect("global_chat")
    else:
        form = PostForm()

    posts = Post.objects.order_by("timestamp")

    decrypted = []
    for p in posts:
        decrypted.append({
            "sender": p.sender.username,
            "timestamp": p.timestamp,
            "text": decrypt_message(p.ciphertext)
        })

    return render(request, "main/chat.html", {
        "posts": decrypted,
        "form": form
    })
