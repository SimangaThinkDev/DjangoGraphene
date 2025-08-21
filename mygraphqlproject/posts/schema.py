# posts/schema.py

import graphene
# A special class from graphene_django that automatically
# converts a django model to a GraphQL type
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import Post
from .filters import PostFilter

class PostType(DjangoObjectType):
    class Meta:
        model = Post
        interfaces = (graphene.relay.Node,)


class CreatePost( graphene.Mutation ):
    class Arguments:
        title = graphene.String( required=True )
        content = graphene.String( required=True )

    
    # The Mutation should return the Post object we just created
    post = graphene.Field( PostType )

    @staticmethod
    def mutate(root, info, **kwargs):
        title = kwargs.get('title')
        content = kwargs.get('content')
        post = Post.objects.create( title=title, content=content )
        return CreatePost( post=post )
    

class Mutation( graphene.ObjectType ):
    create_post = CreatePost.Field()


# --- Update the main schema ---

class Query(graphene.ObjectType):
    post = graphene.relay.Node.Field(PostType)
    # Use our explicit filter class here
    all_posts = DjangoFilterConnectionField(PostType, filterset_class=PostFilter)

    def resolve_all_posts(self, info):
        return Post.objects.all()

    def resolve_post_by_id(root, info, **kwargs):
        pk = kwargs.get('id')
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return None



schema = graphene.Schema(query=Query, mutation=Mutation)
