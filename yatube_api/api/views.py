from django.core.exceptions import PermissionDenied
from posts.models import Comment, Group, Post
from rest_framework import viewsets
from rest_framework.response import Response
from http import HTTPStatus

from .serializers import CommentSerializer, GroupSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(author=self.request.user)
        else:
            raise PermissionDenied(
                "Неавторизованный пользователь не может создавать пост"
            )

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied("Изменение чужого контента запрещено!")
        super(PostViewSet, self).perform_update(serializer)

    def perform_destroy(self, _):
        instance = self.get_object()
        if instance.author != self.request.user:
            raise PermissionDenied("Удаление чужого контента запрещено!")
        instance.delete()


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def create(self, request):
        return Response(
            {"msg": "Не можешь создать группу"},
            status=HTTPStatus.METHOD_NOT_ALLOWED
        )

    # Error message

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied("Изменение чужого контента запрещено!")
        super(CommentViewSet, self).perform_update(serializer)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        return super().get_queryset().filter(post=self.kwargs.get("post_id"))

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post=Post.objects.get(id=(self.kwargs.get("post_id"))),
        )

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied("Изменение чужого контента запрещено!")
        super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, _):
        instance = self.get_object()
        if instance.author != self.request.user:
            raise PermissionDenied("Удаление чужого контента запрещено!")
        instance.delete()
