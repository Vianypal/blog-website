from django.shortcuts import render,get_object_or_404
from django.views import View
from .models import Post,Comment
from django.core.paginator import Paginator
from .forms import LoginForm,UserRegistrationForm
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail,BadHeaderError
from django.http import HttpResponse
from django.db.models import Q

class MainView(View):
    template_name = 'myblog/index.html'
    def get(self, request):
        posts = Post.objects.all()
        paginator = Paginator(posts,6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name,{"page_obj": page_obj})

class PostDetailView(View):
    template_name = 'myblog/blog.html'
    def get(self,request,url_str):
        post = get_object_or_404(Post,url=url_str)
        last_posts = Post.objects.all().order_by('-id')[:5]
        common_tags = post.tag.most_common()
        context={
            "post" : post,
            "last_posts": last_posts,
            "common_tags": common_tags, 
        }
        return render(request,self.template_name,context)
    def post(self,request,url_str):
        post = get_object_or_404(Post,url=url_str)
        comment = request.POST['comment']
        Comment.objects.create(post = post,user=request.user,text=comment)
        return HttpResponseRedirect(reverse('post-detail',args=(url_str,)))

def login_view(request,template_name='myblog/login.html'):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    if request.method == 'GET':
        form  = LoginForm()
        return render(request,template_name,{"form":form})
    if request.method == 'POST':
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = authenticate(username=request.POST['username'],password=request.POST['password'])

            if username is not None:
                login(request,username)
                return HttpResponseRedirect(reverse('index'))
        return render(request,template_name,{"form":form})



def signup_view(request,template_name="myblog/signup.html"):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    form = UserRegistrationForm()
    if request.method=='POST':
        form =UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return HttpResponseRedirect(reverse('index'))
    return render(request,template_name,{"form": form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


class ContactView(View):
    template_name="myblog/contact.html"
    def get(self,request):
        context= {
            "post": {
                "title":"Contact Us",
            }
        }
        return render(request,self.template_name,context)
    def post(self,request):
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        try:
            send_mail(f'From {name} | {subject}', message, email, ['debasish2018rta@gmail.com'])
        except BadHeaderError:
            return HttpResponse('Invalid Header')
        return HttpResponseRedirect(reverse('success'))

def success_view(request,template_name="myblog/success.html"):
    context={
        "post": {
            "title": "Contact Us"
        }
    }
    return render(request,template_name,context)

class SearchResultsView(View):
    def get(self,request):
        query = request.GET['q']
        results = ""
        if query:
            results = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
        else:
            results = Post.objects.all()[:6]
        paginator = Paginator(results,2)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {
            "query": query,
            "page_obj": page_obj,
            "results": results
        }
        return render(request,'myblog/search.html',context)

from taggit.models import Tag
class TagView(View):
    
    def get(self,request,slug):
        tag = get_object_or_404(Tag,slug=slug)
        posts = Post.objects.filter(tag=tag)
        common_tags = Post.tag.most_common()

        context = {
            "title": tag,
            "posts": posts,
            "common_tags" : common_tags
        }
        return render(request,"myblog/tag.html",context)

def delete_comment(request,slug,id):
    comment= Comment.objects.get(pk=id)
    comment.delete()
    return HttpResponseRedirect(reverse('post-detail',args=(slug,)))