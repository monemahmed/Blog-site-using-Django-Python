from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from .models import Post
from.forms import EmailForm
# Create your views here.


# def post_list(request):
#     post_list = Post.published.all()
#     paginator = Paginator(post_list, 3)
#     page = request.GET.get('page')
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     except EmptyPage:
#         posts = paginate.page(paginator.num_pages)
#     return render(request, 'blog/post/list.html', {'posts': posts, 'page': page})

class PostListView(ListView):
    model = 'Post'
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_detail(request, post):
    article = get_object_or_404(Post.published, slug=post)
    return render(request, 'blog/post/detail.html', {'post': article})


def post_share(request, post_id):
    post = get_object_or_404(Post.published, id=post_id)
    url = request.build_absolute_uri(post.get_absolute_url())
    sent = False
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            subject = f"Article Recommendation From {cd['name']}"
            body = f"{cd['name']} recommends you to read this article: \n\" {post.title}\"\nurl: {url} \n Additional Comments: {cd['comment']}.\n Let him Know Your Thoughts at: {cd['email']}"
            send_mail(subject, body, 'moonem.ahmed@gmail.com', [cd['to']]
                      )
            sent = True
    else:
        form = EmailForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})
