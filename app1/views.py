from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Post,Comment
from django.urls import reverse
from django.core.paginator import Paginator,EmptyPage
from django.views.generic import ListView
from .forms import EmailPostForm,CommentForm,CreateBlogForm
from django.core.mail import send_mail
from blog2 import settings
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector,TrigramSimilarity
from django.shortcuts import redirect

def CreateBlogView(request):
    form=CreateBlogForm()
    if request.method=='POST':
        form=CreateBlogForm(request.POST)
        if form.is_valid():
            form.save()
    context={"form":form}
    return render(request,'app1/post/CreateBlog.html',context)

def list_view(request,tag_slug=None):
    post_list=Post.published.all()
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)   #why we are writing this can't we directly pass tag to tags__in=['tag_slug]
        post_list=post_list.filter(tags__in=[tag])
    try:
        paginator = Paginator(post_list, 2) # Show 25 contacts per page.
    except EmptyPage:
        paginator = Paginator(post_list,paginator.num_pages) 

    page_number = request.GET.get('page',1)
    posts= paginator.get_page(page_number)
    return render(request,'app1/post/post_list.html',context={'posts':posts,'tag':tag})
class PostListView(ListView):
    queryset=Post.published.all()
    paginate_by=2
    context_object_name='posts'
    template_name='app1/post/post_list.html'
    

def post_detail(request,id,post):
    post=get_object_or_404(Post,status=Post.Status.PUBLISHED,id=id,slug=post) 
    post_tags_id=post.tags.values_list('id',flat=True)
    similiar_post=Post.published.filter(tags__in=post_tags_id).exclude(id=post.id)    #ye tags us post k h ,,ye usko kaisa pata chala?
    # similiar_post=similiar_post.annotate(same_tags=Count('tags'))\
    #                             .order_by('-same_tags')[:5]

    # try:
    #     post=Post.published.get(id=id,slug=post)
    # except Post.DoesNotExist:
    #     raise Http404('post not found')
    comments=post.comments.all()
    context={'post':post,'comments':comments,'similiar_post':similiar_post}
    return render(request,'app1/post/post_detail.html',context)

def post_share(request,post_id):
    #post=get_object_or_404(Post,status=Post.Status.PUBLISHED,id=post_id)
    #post=get_object_or_404(Post,status=Post.Status.PUBLISHED,id=id) 
    post = get_object_or_404(Post,id=post_id, status=Post.Status.PUBLISHED)
    #post=Post.objects.get(id=3)
    sent=False
    if request.method=='POST':
        form=EmailPostForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            print(cd)
            post_url=request.build_absolute_uri(post.get_absolute_url)
            subject=f"{cd['name']} recommends {post.title}"
            message=f'Here is the link to read {post_url}'
            #send_mail(subject,message,'abcxyzalpha42@gmail.com',[cd['to']])
            #send_mail(subject,message,settings.EMAIL_HOST_USER,[cd['to']])
            send_mail(subject,message,cd['email'],[cd['to']])
            sent=True
    else:
        form=EmailPostForm()
    context={'form':form,'post':post,'sent':sent}
    return render(request,'app1/post/post_share.html',context)



def post_comment(request,post_id):
    post=get_object_or_404(Post,id=post_id,status=Post.Status.PUBLISHED)
    comment=None
    form=CommentForm(request.POST)
    if request.method=='POST':
        if form.is_valid:
            comment=form.save(commit=False)
            comment.post=post
            comment.save()
    context={'post':post,'form':form,'comment':comment}
    return render(request,'app1/post/comment.html',context)

def post_search(request):   #making search
    search_query=request.GET['query']
    search_vector=SearchVector('title',weight='A') +SearchVector('body',weight='B')
    #results=Post.published.annotate(search=SearchVector('title','body')).filter(search=search_query)
    #results=Post.published.annotate(search=search_vector,rank=SearchRank(search_vector,search_query)).filter(search=search_query).order_by('-rank')
    results=Post.published.annotate(similarity=TrigramSimilarity('title',search_query)).filter(similarity__gt=.1).order_by('-similarity')
    context={"results":results,"search_query":search_query}
    return render(request,'app1/search.html',context)







