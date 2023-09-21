
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
from . models import Registrations
class RegistrationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registrations
        fields = '__all__'