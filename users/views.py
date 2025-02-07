from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import login
from .serializers import RegisterSerializer, LoginSerializer, get_tokens_for_user, HotelSerializer, MoviesSerializer, EventsSerializer
from .models import Event, Hotels, Movies
# Create your views here.

class RegisterView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            tokens = get_tokens_for_user(user)
            return Response({
                "message": "User registered successfully.",
                "user": serializer.data,
                "refresh": tokens['refresh'],
                "access": tokens['access']
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            tokens = get_tokens_for_user(user)
            login(request, user)
            return Response({
                "message": "Logged in successfully.",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                },
                "refresh": tokens['refresh'],
                "access": tokens['access']
                }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventView(APIView):
    permissions_classes = [permissions.IsAuthenticated]

    def get(self,request, *args, **kwargs):
        events = Event.objects.all()
        serializer = EventsSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'title': request.data.get('title'),
            'venue': request.data.get('venue'),
            'date': request.data.get('date'),
            'time': request.data.get('time'),
            'price': request.data.get('price'),
            'no_of_tickets': request.data.get('no_of_tickets'),
            'image': request.data.get('image')
        }
        serializer = EventsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EventDetailView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    def get_object(self, event_id):
        try:
            return Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return None
    
    def get(self, request, event_id, *args, **kwargs):
        event_instance = self.get_object(event_id)
        if not event_instance:
            return Response(
                {"res": "Object with event id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = EventsSerializer(event_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, event_id, *args, **kwargs):
        event_instance = self.get_object(event_id)
        if not event_instance:
            return Response(
                {"res": "Event with id does not exist"},
                status=status.HTTP_404_BAD_REQUEST
            )
        data = {
            'title': request.data.get('title'),
            'venue': request.data.get('venue'),
            'date': request.data.get('date'),
            'time': request.data.get('time'),
            'price': request.data.get('price'),
            'image': request.data.get('image'),
            'no_of_tickets': request.data.get('no_of_tickets'),
            'created_at': request.data.get('created_at'),
            'updated_at': request.data.get('updated_at'),
        }
        serializer = EventsSerializer(instance=event_instance, data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, event_id, *args, **kwargs):
        event_instance = self.get_object(event_id)
        if not event_instance:
            return Response(
                {"res": "Event with id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        event_instance.delete()
        return Response(
            {"res": "Event deleted Successfully!"},
            status=status.HTTP_200_OK
        )
    
class MovieView(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        movies = Movies.objects.all()
        serializer = MoviesSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        data = {
            'title': request.data.get('title'),
            'genre': request.data.get('genre'),
            'rating': request.data.get('rating'),
            'price': request.data.get('price'),
            'duration': request.data.get('duration'),
            'date': request.data.get('date'),
            'poster': request.data.get('poster'),
            'no_of_tickets': request.data.get('no_of_tickets'),
        }
        serializer = MoviesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
class MovieDetailView(APIView):
    permisson_classes = []

    def get_object(self, movie_id):
        try:
            return Movies.objects.get(id=movie_id)
        except Movies.DoesNotExist:
            return None
        
    def get(self, request, movie_id, *args, **kwargs):
        movie_instance = self.get_object(movie_id)
        if not movie_instance:
            return Response(
                {"res": "Movie with id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = MoviesSerializer(movie_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, movie_id, *args, **kwargs):
        movie_instance = self.get_object(movie_id)
        if not movie_instance:
            return Response(
                {"res": "Movie with id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'title': request.data.get('title'),
            'genre': request.data.get('genre'),
            'rating': request.data.get('rating'),
            'price': request.data.get('price'),
            'duration': request.data.get('duration'),
            'date': request.data.get('date'),
            'poster': request.data.get('poster'),
            'no_of_tickets': request.data.get('no_of_tickets'),
        }
        serializer = MoviesSerializer(instance=movie_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, movie_id, *args, **kwargs):
        movie_instance = self.get_object(movie_id)
        if not movie_instance:
            return Response(
                {"res": "Movie with id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        movie_instance.delete()
        return Response(
            {"res": "Movie Deleted Successfully!"},
            status=status.HTTP_200_OK
        )
    

class HotelsView(APIView):
    def get(self, request, *args,**kwargs):
        hotels = Hotels.objects.all()
        serializer = HotelSerializer(hotels, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        data ={
            'name': request.data.get('name'),
            'address': request.data.get('address'),
            'price': request.data.get('price'),
            'rating': request.data.get('rating'),
            'image': request.data.get('image')
        }
        serializer = HotelSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class HotelDetailView(APIView):
    permission_classes = []

    def get_object(self, hotel_id):
        try:
            return Hotels.objects.get(id=hotel_id)
        except Hotels.DoesNotExist:
            return None
        
    def get(self, request, hotel_id, *args, **kwargs):
        hotel_instance = self.get_object(hotel_id)
        if not hotel_instance:
            return Response(
                {"res": "Hotel with id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
        )
        serializer = HotelSerializer(hotel_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, hotel_id, *args, **kwargs):
        hotel_instance = self.get_object(hotel_id)
        if not hotel_instance:
            return Response(
                {"res": "Hotel with id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
                )
        data = {
            'name': request.data.get('name'),
            'address': request.data.get('address'),
            'price': request.data.get('price'),
            'rating': request.data.get('rating'),
            'image': request.data.get('image'),
        }
        serializer = HotelSerializer(instance=hotel_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, hotel_id, *args, **kwargs):
        hotel_instance = self.get_object(hotel_id)
        if not hotel_instance:
            return Response(
                {"res": "Hotel with id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        hotel_instance.delete()
        return Response(
            {"res": "Hotel Deleted Successfully"},
            status=status.HTTP_200_OK
        )   