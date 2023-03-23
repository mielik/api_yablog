from django.urls import include, path
from api import views
from rest_framework.authtoken import views
from rest_framework.routers import SimpleRouter

from .views import CommentViewSet, GroupViewSet, PostViewSet

v1_router = SimpleRouter()
v1_router.register("posts", PostViewSet, basename="post")
v1_router.register("groups", GroupViewSet, basename="group")
v1_router.register(
    r"posts/(?P<post_id>\d+)/comments",
    CommentViewSet,
    basename="comments"
)


app_name = "api"

urlpatterns = [
    path("v1/", include(v1_router.urls)),
    path("v1/api-token-auth/", views.obtain_auth_token),
]
