from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework import exceptions, viewsets

from .serializers import CommentSerializer, GroupSerializer, PostSerializer
from posts.models import Group, Post


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_authenticated:
            raise exceptions.NotAuthenticated(
                "Неавторизованный пользователь не может создавать пост"
            )
        serializer.save(author=user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied("Изменение чужого контента запрещено!")
        super().perform_update(serializer)

    def perform_destroy(self, _):
        instance = self.get_object()
        if instance.author != self.request.user:
            raise PermissionDenied("Удаление чужого контента запрещено!")
        instance.delete()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied("Изменение чужого контента запрещено!")
        super().perform_update(serializer)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs.get("post_id"))
        return post.comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post=get_object_or_404(Post, id=(self.kwargs.get("post_id"))),
        )

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied("Изменение чужого контента запрещено!")
        super().perform_update(serializer)

    def perform_destroy(self, _):
        instance = self.get_object()
        if instance.author != self.request.user:
            raise PermissionDenied("Удаление чужого контента запрещено!")
        instance.delete()
