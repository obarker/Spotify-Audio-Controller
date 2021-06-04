from django.urls import path
from .views import RoomView, CreateRoomView, GetRoom

urlpatterns = [
    path('room', RoomView.as_view()),
    path('create', CreateRoomView.as_view()),
    
    #pass params via http://127.0.0.1:8000/api/get-room?code=NWXMFS
    path('get-room', GetRoom.as_view()) 
]