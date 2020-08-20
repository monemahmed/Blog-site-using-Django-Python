from django.utils.safestring import mark_safe
from markdown2 import Markdown
from django import template
from ..models import Post
from django.db.models import Count
register = template.Library()
markdowner = Markdown()


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag('blog/post/most_commented.html')
def most_commented_posts(count=5):
    commented_posts = Post.published.annotate(
        commentsno=Count('comments')).order_by('-commentsno')[:count]
    print(commented_posts)
    return{'commented_post': commented_posts}


@register.inclusion_tag('blog/post/recent_posts.html')
def most_recent(count=5):
    rcps = Post.published.all().order_by('-publish')[:count]
    return {'recent_posts': rcps}


@register.filter(name="markdown")
def markdown_convert(text):
    markdowned = markdowner.convert(text)
    return mark_safe(markdowned)
