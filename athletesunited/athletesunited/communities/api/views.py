from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination

from django.contrib.auth.models import User
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from athletesunited.communities.models import CommunityPost
from athletesunited.communities.api.serializers import CommunityPostSerializer

# Community Post List
class CommunityPostList(generics.ListAPIView):
    model = CommunityPost
    serializer_class = CommunityPostSerializer
    queryset = CommunityPost.objects.order_by('-created_at').all()
    permission_classes = [
        permissions.AllowAny
    ]
    
    def get(self, request, format=None):
        """
        Returns a JSON response with a listing of course objects
        """
        paginator = PageNumberPagination()
        # From the docs:
        # The paginate_queryset method is passed the initial queryset
        # and should return an iterable object that contains only the
        # data in the requested page.
        result_page = paginator.paginate_queryset(self.get_queryset(), request)
        # Now we just have to serialize the data.
        serializer = CommunityPostSerializer(result_page, many=True, context={'request': request})
        # From the docs:
        # The get_paginated_response method is passed the serialized page
        # data and should return a Response instance.
        return paginator.get_paginated_response(serializer.data)





