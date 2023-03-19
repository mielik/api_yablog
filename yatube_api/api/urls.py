from rest_framework.routers import SimpleRouter
from api import views
from django.urls import include, path

from rest_framework.authtoken import views

from .views import PostViewSet, GroupViewSet, CommentViewSet


router = SimpleRouter()
router.register("posts", PostViewSet, basename="post")
router.register("groups", GroupViewSet, basename="group")
router.register(
    r"posts/(?P<post_id>\d+)/comments",
    CommentViewSet,
    basename="comments"
)


app_name = "api"

urlpatterns = [
    path("api/v1/", include(router.urls)),
    path("api/v1/api-token-auth/", views.obtain_auth_token),
]
