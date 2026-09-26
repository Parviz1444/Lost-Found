from django.shortcuts import render, get_object_or_404 , redirect
from .models import Post, Message
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import PostForm
from django.http import HttpResponseForbidden
from django.contrib.auth import get_user_model



def home_view(request):
    posts = Post.objects.select_related("author")
    q = request.GET.get("q")
    if q:
       posts = posts.filter(
           Q(title__icontains=q) | Q(content__icontains=q)
       )
    mine = request.GET.get("mine")
    if mine == "1" and request.user.is_authenticated:
        posts = posts.filter(author=request.user)
    posts = posts.order_by("-created_at")
    return render(request, "adds/home.html", {
        'posts': posts,
        'q': q,
        'mine': mine
    })

@login_required
def post_view(request):
      form = PostForm(request.POST or None, request.FILES or None)
      if request.method == "POST" and form.is_valid():
         post = form.save(commit=False)
         post.author = request.user
         post.save()
         return redirect("post_detail", slug=post.slug)
      return render(request, "adds/form.html", {"form": form})

@login_required
def post_edit(request, slug):
   post = get_object_or_404(Post, slug=slug)
   if post.author != request.user:
       return HttpResponseForbidden("You are not allowed to do this")
   form = PostForm(request.POST or None, request.FILES or None, instance=post)
   if request.method == "POST" and form.is_valid():
       form.save()
       return redirect("post_detail", slug=post.slug)
   return render(request, "adds/form.html", {"form": form})


@login_required
def post_delete(request, slug):
   post = get_object_or_404(Post, slug=slug)

   if post.author != request.user:
       return HttpResponseForbidden("You are not allowed to do this")

   if request.method == "POST":
       post.delete()
       return redirect("home")
   return render(request, "adds/post_delete_confirm.html", {"post": post})


def post_detail_view(request, slug):
    post = get_object_or_404(Post.objects.select_related("author"), slug=slug)
    return render(request, "adds/detail.html", {"post": post})

@login_required
def notifs_view(request):
    latest = Message.objects.filter(Q(sender=request.user) | Q(recipient=request.user)).select_related("post", "sender", "recipient").order_by("-created_at")
    conversations = {}
    for message in latest:
        peer = message.recipient if message.sender_id == request.user.id else message.sender
        key = (message.post_id, peer.id)
        if key not in conversations:
            conversations[key] = {"post": message.post, "person": peer, "latest": message, "unread": 0}
        if message.recipient_id == request.user.id and not message.is_read:
            conversations[key]["unread"] += 1
    return render(request, "adds/notifs.html", {"conversations": conversations.values()})

@login_required
def profile(request):
    return render(request, "adds/profile.html", {"profile_user": request.user, "post_count": request.user.posts.count()})

def user_profile(request, username):
    from django.contrib.auth import get_user_model
    person = get_object_or_404(get_user_model(), username=username)
    return render(request, "adds/profile.html", {"profile_user": person, "post_count": person.posts.count()})

@login_required
def message_view(request, slug):
    post = get_object_or_404(Post.objects.select_related("author"), slug=slug)
    if not post.author:
        return HttpResponseForbidden("This listing has no author to contact.")
    peer_id = request.GET.get("with") or request.POST.get("with")
    if peer_id:
        peer = get_object_or_404(get_user_model(), pk=peer_id)
    elif post.author_id != request.user.id:
        peer = post.author
    else:
        prior = Message.objects.filter(post=post, recipient=request.user).order_by("-created_at").first()
        if not prior:
            return redirect("notifs")
        peer = prior.sender
    if peer == request.user or (peer != post.author and not Message.objects.filter(post=post).filter(
        Q(sender=request.user, recipient=peer) | Q(sender=peer, recipient=request.user)
    ).exists()):
        return HttpResponseForbidden("This conversation is not available.")
    if request.method == "POST":
        body = request.POST.get("body", "").strip()
        if body and len(body) <= 2000:
            Message.objects.create(post=post, sender=request.user, recipient=peer, body=body)
            return redirect(f"/posts/{post.slug}/message/?with={peer.id}")
    messages = Message.objects.filter(post=post).filter(
        Q(sender=request.user, recipient=peer) | Q(sender=peer, recipient=request.user)
    ).select_related("sender")
    messages.filter(recipient=request.user, is_read=False).update(is_read=True)
    return render(request, "adds/message.html", {"post": post, "author": peer, "messages": messages, "peer": peer})
