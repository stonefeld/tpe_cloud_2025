from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from .views import PoolViewSet, RequestViewSet

router = DefaultRouter()
router.register(r"", PoolViewSet, basename="pool")

pools_router = NestedDefaultRouter(router, r"", lookup="pool")
pools_router.register(r"requests", RequestViewSet, basename="pool-requests")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(pools_router.urls)),
]
