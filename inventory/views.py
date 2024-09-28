from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from .models import Item
from .serializers import ItemSerializer, Userserializer
import logging
from django.contrib.auth.models import User
from rest_framework import generics


logger = logging.getLogger(__name__)

class ItemView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, item_id=None):
        if item_id:
            cache_key = f'item_{item_id}'
            item = cache.get(cache_key)
            
            if not item:
                try:
                    item = Item.objects.get(id=item_id)
                    cache.set(cache_key, item)
                except Item.DoesNotExist:
                    return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

            serializer = ItemSerializer(item)
            return Response(serializer.data)
        else:
            items = Item.objects.all()
            serializer = ItemSerializer(items, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, item_id):
        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete(f'item_{item_id}')
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, item_id):
        try:
            item = Item.objects.get(id=item_id)
            item.delete()
            cache.delete(f'item_{item_id}')
            return Response({'message': 'Item deleted'}, status=status.HTTP_200_OK)
        except Item.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

class UserView(generics.ListCreateAPIView):
    queryset =User.objects.all()
    serializer_class = Userserializer