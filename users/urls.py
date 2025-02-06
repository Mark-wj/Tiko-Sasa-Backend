from django.urls import path
from .views import RegisterView, LoginView, EventView, EventDetailView, MovieView, MovieDetailView, HotelsView, HotelDetailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('events/', EventView.as_view(), name='events'),
    path('events/<int:event_id>/', EventDetailView.as_view(), name='Event Detail View'),
    path('movies/', MovieView.as_view(), name="movies"),
    path('movies/<int:movie_id>/', MovieDetailView.as_view(), name='Movie Detail View'),
    path('hotels/', HotelsView.as_view(), name='hotels'),
    path('hotels/<int:hotel_id>/', HotelDetailView.as_view(), name='Hotel Detail')
]
