from rest_framework.generics import CreateAPIView
from .serializers import ServiceProviderSerializer


class CreateServiceProvider(CreateAPIView):
    serializer_class = ServiceProviderSerializer



