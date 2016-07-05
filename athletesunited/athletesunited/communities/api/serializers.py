from django.contrib.auth.models import User

from rest_framework import serializers

from athletesunited.communities.models import CommunityPost

# Community Post Serializer
class CommunityPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommunityPost
        fields = ('body', 'created_at', 'community', 'city', 'verified_users', 'spam_count', )




