from rest_framework import serializers
from .models import Room

#serializer json-ifies selected data.

#serializes room data
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id','code','host','guest_can_pause','votes_to_skip','created_at')

#serializes public properties thats can be changed / set when room is made. more efficient than passing the whole room json.
class CreateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('guest_can_pause','votes_to_skip')

        
