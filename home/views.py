from .serializers import BlogSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Blog
from django.db.models import Q
from django.core.paginator import Paginator


#api view for public
class PublicBlog(APIView):
    permission_classes = [AllowAny]

    def get(self,request):
        try:
            blogs = Blog.objects.all().order_by('?')

            if request.GET.get('search'):
                search = request.GET.get('search')
                blogs = blogs.filter(Q(title__icontains = search) | Q(blog_text__icontains = search))
            
            page_number = request.GET.get('page',1)
            paginator = Paginator(blogs, 1)

            serializer = BlogSerializer(paginator.page(page_number), many=True)

            return Response({
                'data': serializer.data,
                'message':'Blogs fetched successfully',
            },status = status.HTTP_201_CREATED)
        
        except Exception as e:
             return Response({
                    'data': {},
                    'message': 'Something went wrong or Invalid page',
                },status = status.HTTP_400_BAD_REQUEST)


#api view for only authorized user, an user can create,update or delete a blog
class BlogView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    #code for view blog
    def get(self,request):
        try:
            print(request.user)
            blogs = Blog.objects.filter(user = request.user)

            #search a blog by title and blog text
            if request.GET.get('search'):
                search = request.GET.get('search')
                blogs = blogs.filter(Q(title__icontains = search) | Q(blog_text__icontains = search))
                
            serializer = BlogSerializer(blogs, many=True)

            return Response({
                'data': serializer.data,
                'message':'Blogs fetched successfully',
            },status = status.HTTP_201_CREATED)
        
        except Exception as e:
             return Response({
                    'data': {},
                    'message': 'Something went wrong',
                },status = status.HTTP_400_BAD_REQUEST)

    #code for create a blog - Only authorized user
    def post(self,request):
        try:
            data = request.data
            data['user'] = request.user.id
            serializer = BlogSerializer(data = data)
            if serializer.is_valid():  
                return Response({
                    'data': serializer.data,
                    'message': 'Blog created Successfully',
                },status = status.HTTP_201_CREATED)
            
            return Response({
                    'data': serializer.errors,
                    'message': 'Something went wrong',
                },status = status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
             return Response({
                    'data': {},
                    'message': 'Something went wrong',
                },status = status.HTTP_400_BAD_REQUEST)
        
    #code for Update a Blog - Only authorized user
    def patch(self,request):
        try:
            data = request.data 
            blog = Blog.objects.filter(uid = data.get('uid'))
            
            if not blog.exists():
                return Response({
                    'data':{},
                    'message':"Invalid Blog uid",
                },status = status.HTTP_400_BAD_REQUEST)
        
            #usage - This kind of check is typically used to determine if the logged-in user has permission to perform certain actions on a blog post, such as editing or deleting it. If the users don't match, the action might be restricted.
            if request.user != blog[0].user:
                return Response({
                    'data':{},
                    'message':"You are not authorozed to this",
                },status = status.HTTP_400_BAD_REQUEST)
            
            serializer = BlogSerializer(blog[0],data = data, partial = True)
            if serializer.is_valid():  
                serializer.save()
                return Response({
                    'data': serializer.data,
                    'message': 'Blog Updated Successfully',
                },status = status.HTTP_201_CREATED)
            
            return Response({
                    'data': serializer.errors,
                    'message': 'Something went wrong',
                },status = status.HTTP_400_BAD_REQUEST)

        except Exception as e:
             return Response({
                    'data': {},
                    'message': 'Something went wrong',
                },status = status.HTTP_400_BAD_REQUEST)
        
    #code for delete a blog - Only authorized user
    def delete(self,request):
        try:
            data = request.data 
            blog = Blog.objects.filter(uid = data.get('uid'))
            
            if not blog.exists():
                return Response({
                    'data':{},
                    'message':"Invalid Blog uid",
                },status = status.HTTP_400_BAD_REQUEST)
            
            if request.user != blog[0].user:
                return Response({
                    'data':{},
                    'message':"You are not authorozed to this",
                },status = status.HTTP_400_BAD_REQUEST)
            
            blog[0].delete()
            return Response({
                    'data': {},
                    'message': 'Blog Deleted Successfully',
                },status = status.HTTP_400_BAD_REQUEST)

        except Exception as e:
             return Response({
                    'data': {},
                    'message': 'Something went wrong',
                },status = status.HTTP_400_BAD_REQUEST)
            
    
        





