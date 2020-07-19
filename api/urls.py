from .generators import router_generator

router = router_generator()
urlpatterns = router.urls
