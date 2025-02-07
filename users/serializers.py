from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Event, Hotels, Movies

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password', 'password2')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords must match!")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        if not email or not password:
            raise serializers.ValidationError("Email and password are required")
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid Credentials.")
        data['user'] = user
        return data
    
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [            'title',
            'venue',
            'date',
            'time',
            'price',
            'image',
            'no_of_tickets']

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotels
        fields = '__all__'

class MoviesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
        fields = '__all__'
        