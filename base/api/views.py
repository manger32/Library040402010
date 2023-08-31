from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Authorize
from .serializers import AuthSerializer
@api_view(['GET'])
def get_Routes(request):
    routes = [
        'GET /api',
        'GET /api/Authorize',
        'GET /api/Authorize/:id'
    ]
    return Response(routes)


@api_view(['GET'])
def get_Authorizes(request):
    auth_id_id = Authorize.objects.all()
    serializer = AuthSerializer(auth_id_id, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_Authorize(request, pk):
    auth_id_id = Authorize.objects.get(id=pk)
    serializer = AuthSerializer(auth_id_id, many=False)
    return Response(serializer.data)