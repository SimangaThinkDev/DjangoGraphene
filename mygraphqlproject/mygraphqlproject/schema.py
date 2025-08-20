# mygraphqlproject/schema.py

import graphene
from graphene_django import DjangoObjectType
from posts.models import Post


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'published_date')


class Query(graphene.ObjectType):
    all_posts = graphene.List( PostType )
    post_by_id = graphene.Field( PostType, id=graphene.Int() )

    def resolve_all_posts( self, info ):
        return Post.objects.all()

    def resolve_post_by_id( self, info, id ):
        try:
            return Post.objects.get(pk=id)
        except Post.DoesNotExist:
            return None

schema = graphene.Schema(query=Query)
