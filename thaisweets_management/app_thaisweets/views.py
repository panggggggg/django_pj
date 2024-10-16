from django.http import HttpRequest , HttpResponseForbidden
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import FormView
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.contrib import messages
from app_thaisweets.forms import *
from .models import *
from django.views import View
# from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
# from .filters import PostFilter
from django.db.models import Q
import os

class SignupPage(View):
    def get(self, request):
        form = SignupModelForm()
        return render(request, 'signup.html',{'form': form})
    
    def post(self, request):
        #! สร้างฟอร์มโดยรับข้อมูลจากผู้ใช้ที่ทำการกดปุ่ม
        form = SignupModelForm(request.POST)
        if form.is_valid():
            user = form.save()
            #! ทำการloginผู้ใช้ที่เพิ่งสร้างขึ้นทันที
            login(request, user)
            return redirect('blog')
        return render(request, 'signup.html',{'form': form})

class LoginPage(View):
    def get(self, request):
        form = SigninModelForm()
        return render(request, 'registration/login.html', {'form': form})

    def post(self, request):
        #! สร้างฟอร์มโดยรับข้อมูลจากผู้ใช้ที่ทำการกดปุ่ม
        form = SigninModelForm(request.POST) 
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('blog') 
            else:
                messages.error(request, "Invalid Username or Password")  
                form = SigninModelForm()

        return render(request, 'registration/login.html', {'form': form})

class HomePage(View):
    def get(self, request):
        return render(request, 'home.html')

class LogoutPage(View):
    def get(self, request):
        logout(request)
        return render(request, 'home.html')
    
class PostPage(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self, request):
        form = PostModelForm()
        return render(request, 'post.html', {'form': form})
    
    def post(self, request):
        #! request.FILES = รับค่าข้อมูลรูปแบบไฟล์ด้วย
        form = PostModelForm(request.POST,request.FILES)
        if form.is_valid():
            form_post = form.save(commit=False)
            form_post.user = request.user
            form_post.save()

            #! Get category ids จากการเลือกและเซตเข้าdb เป็นการเซตแบบ mtom
            category_ids = form.cleaned_data['Category']
            form_post.category_set.set(category_ids)

            return redirect('blog')
        data = {'form': form}
        return render(request, 'post.html', data)
class BlogPage(View):
    def get(self, request):
        # ! syntax query in manytomany table use __ follow field name like -> field "name" is use category_set__name
        # query = Post.objects.values("title", "body", "image", "category_set__name","post_id").order_by('-created_at')
        query = Post.objects.prefetch_related('category_set').order_by('-created_at')
        data = {
            "blogs": query, 
        }
        return render(request, "blog.html", data)
    

class ProfilePage(LoginRequiredMixin, FormView):
    login_url = 'login'
    template_name = 'profile.html'
    success_url = 'profile'  # URL to redirect after successful form submission
    form_class = ProfileModelForm  # Base form for the user

    # You can use get_context_data to pass multiple forms to the template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Pass both forms to the template
        context['base_form'] = self.get_form(ProfileModelForm)
        try:
            context['base_form'] = ProfileModelForm(instance=user)
            context['extend_form'] = ExtendProfileForm(instance=user.userprofile)
        except:
            context['extend_form'] = ExtendProfileForm()

        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        user_profileform = ProfileModelForm(request.POST, instance=user)

        # Try to get the profileuser instance or create a new one
        try:
            extended_user = ExtendProfileForm(request.POST,request.FILES, instance=user.userprofile)
            is_newProfile = False
        except:
            extended_user = ExtendProfileForm(request.POST,request.FILES)
            is_newProfile = True

        # Validate both forms
        if user_profileform.is_valid() and extended_user.is_valid():
            # Save user profile form
            user_profileform.save()

            if is_newProfile:
                # Create new profile user if it's a new profile
                profile = extended_user.save(commit=False)
                profile.user = user
                profile.save()
            else:
                # Update existing profile
                extended_user.save()

            return redirect(self.success_url)

        # If the forms are not valid, render the form with errors
        return self.form_invalid(user_profileform, extended_user)

    def form_invalid(self, user_profileform, extended_user):
        return self.render_to_response(
            self.get_context_data(base_form=user_profileform, extend_form=extended_user)
        )
    

class SearchPage(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self, request):
        text_search = request.GET.get('text_search', '')
        if text_search:
            query = Post.objects.filter(
                Q(category_set__name__icontains=text_search) | Q(title__icontains=text_search)).order_by('-created_at')
        else:
            query = Post.objects.order_by('-created_at')
        return render(request, "search.html", {"blogs": query})
        

class post_detail(View,PermissionRequiredMixin,LoginRequiredMixin):
    login_url = 'login'
    # permission_required = ["blogs.view_blog"]
    def get(self,request: HttpRequest, post_id):
        blog = get_object_or_404(Post, post_id=post_id)
        comments = blog.comments.all()

        # Get the total share count by summing up the 'count' field
        total_shares = Share.objects.filter(post=blog).aggregate(Sum('count'))['count__sum'] or 0

        context = {
            'blog': blog,
            'comments': comments,
            'total_shares': total_shares,
        }

        return render(request, 'post_detail.html', context)

class post_comments(LoginRequiredMixin, View):
    login_url = 'login'  # Redirect to login if not authenticated
    
    def get(self, request, post_id):
        post = get_object_or_404(Post, post_id=post_id)
        comments = post.comments.all()  # Retrieve all comments for the post
        form = CommentForm()  # Empty form for GET request

        return render(request, 'post_comments.html', {
            'post': post,
            'comments': comments,
            'form': form
        })

    def post(self, request, post_id):
        post = get_object_or_404(Post, post_id=post_id)
        comments = post.comments.all()  # Retrieve all comments for the post
        form = CommentForm(request.POST)  # Bind form with POST data

        if form.is_valid():
            comment = form.save(commit=False)  # Create comment but don't save yet
            comment.post = post  # Link comment to the post
            comment.user = request.user  # Link comment to the user
            comment.save()  # Save the comment
            return redirect('post_comments', post_id=post_id)  # Refresh the page after comment is posted

        return render(request, 'post_comments.html', {
            'post': post,
            'comments': comments,
            'form': form
        })
    
class Share_post(LoginRequiredMixin, View):
    login_url = 'login'  # Redirect to login if not authenticated

    def post(self, request, post_id):
        post = get_object_or_404(Post, post_id=post_id)

        if request.user.is_authenticated:
        # Check if the user has already shared the post
            if not Share.objects.filter(post=post, user=request.user).exists():
            # Create a new share entry with count incremented
                Share.objects.create(post=post, user=request.user, count=1)
            else:
                # If user has already shared, update the count
                share = Share.objects.get(post=post, user=request.user)
                share.count += 1
                share.save()
       

        return redirect('post_detail', post_id=post_id)  # Redirect to post detail page

# def is_my_post(user, author):
#     if user == author:
#         return True
#     return False



        # if not is_my_post(request.user, post.author):
        #     if not request.user.is_staff:
        #         raise PermissionDenied("Only for the blog owner.")
            

# class PostDeleteView(LoginRequiredMixin,PermissionRequiredMixin,View):
#     login_url = 'login'
#     permission_required = ["post.delete_post"]  

#     def get(self, request: HttpRequest, post_id):
#         post = get_object_or_404(Post, pk=post_id)

#         post.delete()
#         return redirect('blog')
        
class PostDeleteView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request: HttpRequest, post_id):
        post = get_object_or_404(Post, pk=post_id)

        # Check if the logged-in user is the author of the post or is a staff member
        if request.user == post.user or request.user.has_perm('post.delete_post'):
            post.delete()
            return redirect('blog')
        else:
            return HttpResponseForbidden("You are not allowed to delete this post.")
