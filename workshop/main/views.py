from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view , permission_classes
from .models import Post
from django.db.models import Q
from .serializers import PostSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
@api_view(['GET'])
def home(request):
    return Response({'hello':'world'})


@api_view(['GET'])
def posts(request):
    all_posts = Post.objects.all()
    post_ser = PostSerializer(all_posts,many= True)
    return Response({'posts':post_ser.data},status=status.HTTP_200_OK)



@api_view(['POST'])
def addPost(request):
    post_ser = PostSerializer(data=request.data)
    if post_ser.is_valid():
        post_ser.save()
        return Response({'success':'post added'},status=status.HTTP_201_CREATED)
    return Response({'error':post_ser.errors})


from django.shortcuts import get_object_or_404
@api_view(['GET','PUT','DELETE'])
def PostDetails(request,id):
    inst = get_object_or_404(Post,id=id)
    if request.method == 'GET':
        post_ser = PostSerializer(inst)
        return Response(post_ser.data)

    elif request.method == 'PUT':
       
        post_ser = PostSerializer( inst,request.data ,partial= True)
        if post_ser.is_valid():
            post_ser.save()
            return Response({'success':'post modified'},status=status.HTTP_200_OK)
        return Response({'error':post_ser.errors})
    
    elif request.method == 'DELETE':
        inst.delete()
        return Response({'success':'deletion was successful'})



from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import CustomUserSerializer
@api_view(['POST'])
def register(request):
    user_ser = CustomUserSerializer(data=request.data)
    if user_ser.is_valid():
        user = user_ser.save()
        refresh = RefreshToken.for_user(user)

        context = {
            'details' : user_ser.data,
            'success' : 'user created successfully',
            'refresh' : str(refresh),
            'access' :  str(refresh.access_token)
        }
        return  Response(context, status=status.HTTP_201_CREATED)
    return Response(user_ser.errors, status=status.HTTP_400_BAD_REQUEST)

 
from django.contrib.auth import authenticate

@api_view(['POST'])
def login(request):
    username_or_email = request.data.get('email')
    password = request.data.get('password')

    if not username_or_email or not password:
        return Response({"error": "Email/Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(email=username_or_email, password=password)

    if not user:
        # Try authenticating by username
        try:
            email = User.objects.get(username=username_or_email).email
            user = authenticate(email=email, password=password)
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
    if user:
        refresh = RefreshToken.for_user(user)
        tokens = {
            'refresh' : str(refresh),
            'access' : str(refresh.access_token)
        }
        return Response(tokens, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)





@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({'success':'u can view this page'})

 

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    refresh_token = request.data['refresh']
    if not refresh_token:
        return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()  # Blacklist the refresh token
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
    except :
        return Response({'error': 'something happened'}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['post'])
def get_refresh(request):
    access = str(  RefreshToken(request.data['refresh']).access_token  )
    return Response({'access':access})