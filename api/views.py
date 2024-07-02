# Create your views here.
from rest_framework import mixins, generics
from rest_framework.permissions import IsAuthenticated
from viewer.models import Mushroom, Family, Recipe, Finding
from .serializers import MushroomSerializer, FamilySerializer, RecipeSerializer, FindingSerializer


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