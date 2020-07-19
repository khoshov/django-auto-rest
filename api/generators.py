from django.apps import apps
from django_filters import rest_framework as filters
from rest_framework import viewsets, serializers, routers

from .pagination import CustomLimitOffsetPagination
from .utils import get_prefix


def serializer_class_generator(model):
    meta = type('Meta', (), {'model': model, 'fields': '__all__'})
    return type(
        f'{model.__name__}Serializer',
        (serializers.ModelSerializer,),
        {'Meta': meta},
    )


def filterset_class_generator(model):
    fields = [(field.name, field.name) for field in model._meta.fields]
    ordering = filters.OrderingFilter(fields=fields)
    meta = type('Meta', (), {'model': model, 'fields': '__all__'})
    return type(
        f'{model.__name__}FilterSet',
        (filters.FilterSet,),
        {'ordering': ordering, 'Meta': meta},
    )


def viewset_class_generator(model, serializer, filterset):
    attrs = {
        'queryset': model.objects.all(),
        'serializer_class': serializer,
        'filter_backends': (filters.DjangoFilterBackend,),
        'filterset_class': filterset,
        'pagination_class': CustomLimitOffsetPagination,
    }
    return type(f'{model.__name__}ViewSet', (viewsets.ModelViewSet,), attrs)


def router_generator():
    router = routers.SimpleRouter()
    for app in apps.get_app_configs():
        for model in app.get_models():
            serializer = serializer_class_generator(model)
            filterset = filterset_class_generator(model)
            viewset = viewset_class_generator(model, serializer, filterset)
            prefix = get_prefix(app, model)
            router.register(prefix, viewset)
    return router
