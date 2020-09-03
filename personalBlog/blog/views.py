from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from .models import Post, Comment
from taggit.models import Tag
from django.db.models import Count
from.forms import EmailForm, CommentForm
# Create your views here.


def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    paginator = Paginator(post_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginate.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'posts': posts, 'page': page, 'tag': tag})

# class PostListView(ListView):
#     model = 'Post'
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'blog/post/list.html'


def post_detail(request, post):
    article = get_object_or_404(Post.published, slug=post)
    # calculating Similar Posts
    tag_ids = article.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(
        tags__in=tag_ids).exclude(id=article.id)
    similar_posts = similar_posts.annotate(
        same_tags=Count('tags')).order_by('-same_tags', '-publish')[:3]

    comments = article.comments.filter(post=article.id)
    new_comment = None
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_comment = form.save(commit=False)
            new_comment.post = article
            new_comment.save()
            form = CommentForm()
    else:
        form = CommentForm()

    return render(request, 'blog/post/detail.html', {'comments': comments, 'form': form, 'new_comment': new_comment, 'post': article, 'similar': similar_posts})


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
