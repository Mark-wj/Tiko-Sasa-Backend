from django.urls import path
from .views import RegisterView, LoginView, EventView, EventDetailView, MovieView, MovieDetailView, HotelsView, HotelDetailView,  HotelGalleryListCreateView, HotelGalleryDetailView, MovieCastDetailView, MovieCastListCreateView
from .views import create_checkout_session


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('events/', EventView.as_view(), name='events'),
    path('events/<int:event_id>/', EventDetailView.as_view(), name='Event Detail View'),
    path('movies/', MovieView.as_view(), name="movies"),
    path('movies/<int:movie_id>/', MovieDetailView.as_view(), name='Movie Detail View'),
    path('movie-cast/', MovieCastListCreateView.as_view(), name='movie-cast-list-create'),
    path('api/movies/<int:pk>/', MovieCastDetailView.as_view(), name='movie-detail'),
    path('hotels/', HotelsView.as_view(), name='hotels'),
    path('hotels/<int:hotel_id>/', HotelDetailView.as_view(), name='Hotel Detail'),
    path("stripe/create-checkout-session/", create_checkout_session, name="checkout"),
    path('hotel-galleries/', HotelGalleryListCreateView.as_view(), name='hotel-gallery-list-create'),
    path('hotel-galleries/<int:pk>/', HotelGalleryDetailView.as_view(), name='hotel-gallery-detail'),
]

# ma