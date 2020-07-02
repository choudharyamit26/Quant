from rest_framework import serializers
from restapi.models import ElectricityProvider


class ServiceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectricityProvider
        fields = (
            "electricity_provider_code",
            "electricity_provider_name"
        )
