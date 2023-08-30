from  rest_framework.serializers import ModelSerializer
from base.models import Authorize

class AuthSerializer(ModelSerializer):
    class Meta:
        model = Authorize
        fields = '__all__'