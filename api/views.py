# views.py
from django.views.decorators.csrf import csrf_exempt
from rest_framework import mixins, generics
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from viewer.models import Mushroom, Family, Recipe, Finding, Habitat
from accounts.models import Profile
from .serializers import MushroomSerializer, FamilySerializer, RecipeSerializer, FindingSerializer, HabitatSerializer, \
    ProfileSerializer
from rest_framework.authtoken.serializers import AuthTokenSerializer


class Mushrooms(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Mushroom.objects.all()
    serializer_class = MushroomSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class Families(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Family.objects.all()
    serializer_class = FamilySerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class Recipes(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class Findings(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Finding.objects.all()
    serializer_class = FindingSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class Habitats(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Habitat.objects.all()
    serializer_class = HabitatSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class Profiles(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key})
