# posts/schema.py

import graphene
# A special class from graphene_django that automatically
# converts a django model to a GraphQL type
from graphene_django import DjangoObjectType
from .models import Post

class PostType( DjangoObjectType ):
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'published_date')
