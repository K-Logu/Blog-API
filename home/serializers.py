from rest_framework import serializers
from .models import Blog


#serializer for user blog
class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        exclude = ['created_at','updated_at']
        