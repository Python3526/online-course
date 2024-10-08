from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from blogs.forms import CommentForm
from blogs.models import Blog
from courses.models import Category, Comment


class BlogsPage(View):
    def get(self, request):
        blogs = Blog.objects.all()
        categories = Category.objects.annotate(course_count=Count('courses'))
        num_of_categories = len(categories)

        paginator = Paginator(blogs, 2)

        page_number = request.GET.get('page')
        blogs = paginator.get_page(page_number)

        context = {'blogs': blogs,
                   'categories': categories,
                   'num_of_categories': num_of_categories,
                   'active_page': 'blog'}

        return render(request, 'blogs/blog.html', context)


class SinglePage(View):
    def get(self, request):
        blog = Blog.objects.order_by('-created_at').first()
        categories = Category.objects.annotate(course_count=Count('courses'))
        comments = Comment.objects.filter(blog_id__slug=blog.slug).order_by('-created_at')
        num_of_categories = len(categories)

        context = {'blog': blog,
                   'categories': categories,
                   'comments': comments,
                   'num_of_categories': num_of_categories,
                   'active_page': 'blog'}

        return render(request, 'blogs/blog_detail.html', context)


class BlogDetail(View):
    def get(self, request, slug):
        blogs = Blog.objects.all()
        blog = Blog.objects.get(slug=slug)
        comments = Comment.objects.filter(blog_id__slug=slug).order_by('-created_at')
        categories = Category.objects.annotate(course_count=Count('courses'))

        context = {'blog': blog,
                   'blogs': blogs,
                   'categories': categories,
                   'comments': comments,
                   'active_page': 'blog'}

        return render(request, 'blogs/blog_detail.html', context)


class AddComment(View):
    def get(self, request, slug):
        form = CommentForm()
        return render(request, 'blogs/blog_detail.html', {'form': form, 'slug': slug})

    def post(self, request, slug):
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            blog_id = get_object_or_404(Blog, slug=slug)

            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            comment = form.cleaned_data['comment']
            rating = form.cleaned_data['rating']
            media_file = form.cleaned_data['media_file']

            if media_file:
                comment = Comment(name=name, email=email, rating=rating, comment=comment, blog_id=blog_id,
                                  media_file=media_file)
            else:
                comment = Comment(name=name, email=email, rating=rating, comment=comment, blog_id=blog_id)

            comment.save()

            return redirect('single', slug=slug)
        return redirect('single', slug=slug)


class DeleteComment(View):
    def get(self, request, slug):
        comment_id = request.GET.get('comment_id')
        comment = get_object_or_404(Comment, id=comment_id)
        comment.delete()
        return redirect('single', slug=slug)
