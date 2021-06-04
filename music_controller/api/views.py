from django.shortcuts import render
from rest_framework import generics, status
from .serializers import RoomSerializer, CreateRoomSerializer
from .models import Room
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.

#lists all room objects that have been serialized.
class RoomView(generics.ListAPIView):                                                                           
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class GetRoom(APIView): #get the current room data.
    serializer_class = RoomSerializer
    lookup_url_kwarg = 'code'


#define get / read function to API.
    def get(self, request, format=None):         
#finds the roomCode in the URL                                                                     
        code = request.GET.get(self.lookup_url_kwarg)    
# if code doesnt exist then HTTP 400 bad request.                                                            
        if code != None:            
# using code in URL, it searches for the room objects.                                                                                 
            room = Room.objects.filter(code=code)                                                                     
            if len(room) > 0:                                                                                        
                data = RoomSerializer(room[0]).data 
# if the client session ID == room host ID then they are host.                                                                 
                data['is_host'] = self.request.session.session_key == room[0].host                                   
                return Response(data, status=status.HTTP_200_OK)                                                    
            return Response({'Room Not Found': 'Invalid Room Code.'}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({'Bad Request': 'Code paramater not found in request'}, status=status.HTTP_400_BAD_REQUEST)


 # django html form / api view to create a room
class CreateRoomView(APIView):                                                                                     
    serializer_class = CreateRoomSerializer                                                                         

    def post(self, request, format=None):                  
# if client session / key doesnt exist, make one.                                                         
        if not self.request.session.exists(self.request.session.session_key):                                       
            self.request.session.create()

        serializer = self.serializer_class(data=request.data)                                                       
        if serializer.is_valid():
# set room properties to input of of API
            guest_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')
            host = self.request.session.session_key
            queryset = Room.objects.filter(host=host)
# queryset is list of all rooms, if it is exists, check for current room and update properties.
            if queryset.exists():
                room = queryset[0]
                room.guest_can_pause = guest_can_pause
                room.votes_to_skip = votes_to_skip
                room.save(update_fields=['guest_can_pause', 'votes_to_skip'])
                return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
# else make room and add properties to room.
            else:
                room = Room(host=host, guest_can_pause=guest_can_pause,
                            votes_to_skip=votes_to_skip)
                room.save()
                return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)