import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import login
from .serializers import RegisterSerializer, LoginSerializer, get_tokens_for_user, HotelSerializer, MoviesSerializer, EventsSerializer, HotelGallerySerializer, CastSerializer
from .models import Event, Hotels, Movies, HotelGallery, MovieCast
# Create your views here.
stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def create_checkout_session(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "product_data": {"name": data["product"]},
                            "unit_amount": int(data["amount"]) * 100,  # Convert to cents
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",
                success_url="http://localhost:3000/success",
                cancel_url="http://localhost:3000/cancel",
            )
            return JsonResponse({"id": session.id})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)

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

class HotelGalleryListCreateView(APIView):
    """
    List all gallery images or create a new gallery image for a hotel.
    """

    def get(self, request, format=None):
        galleries = HotelGallery.objects.all()
        serializer = HotelGallerySerializer(galleries, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = HotelGallerySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HotelGalleryDetailView(APIView):
    """
    Retrieve, update, or delete a gallery image instance.
    """

    def get_object(self, pk):
        return get_object_or_404(HotelGallery, pk=pk)

    def get(self, request, pk, format=None):
        gallery = self.get_object(pk)
        serializer = HotelGallerySerializer(gallery)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        gallery = self.get_object(pk)
        serializer = HotelGallerySerializer(gallery, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        gallery = self.get_object(pk)
        gallery.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MovieCastListCreateView(APIView):
    """
    API view to retrieve list of cast members or create a new cast member.
    """

    def get(self, request, format=None):
        cast_members = MovieCast.objects.all()
        serializer = CastSerializer(cast_members, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CastSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MovieCastDetailView(APIView):
    """
    API view to retrieve, update, or delete a specific cast member.
    """

    def get_object(self, pk):
        return get_object_or_404(MovieCast, pk=pk)

    def get(self, request, pk, format=None):
        cast_member = self.get_object(pk)
        serializer = CastSerializer(cast_member)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        cast_member = self.get_object(pk)
        serializer = CastSerializer(cast_member, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        cast_member = self.get_object(pk)
        cast_member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)