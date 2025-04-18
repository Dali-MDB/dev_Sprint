from rest_framework import serializers
from .models import Post,CustomUser

from django.contrib.auth import get_user_model

User = get_user_model()



class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    class Meta:
        model = CustomUser
        fields = ['id','username','email','password','phone_number']


    def validate(self, data):
        email = data.get("email")
        username = data.get("username")
        phone_number = data.get("phone_number")
        password = data.get('password')

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "A user with this email already exists."})

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"username": "This username is already taken."})

        if User.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError({"phone_number": "This phone number is already registered."})
        
        def is_strong_password(pasword):
            if (
                len(password) < 8 or 
                not any(char.islower() for char in pasword) or  
                not any(char.isupper() for char in pasword)
            ):
                return False
            return True

        if not is_strong_password(password):
            raise serializers.ValidationError({'password' : 'the password you have provided is too weak'})

        return data
    
    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

    
    def update(self, instance, validated_data):
        password = validated_data.pop('password',None)

        for key,value in validated_data.items():
            setattr(instance,key,value)

        

        if password:
            instance.set_password(password)

        return instance



class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','title','description','image']
