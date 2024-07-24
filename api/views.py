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
    """
    API view to retrieve list of mushrooms or create a new mushroom.

    Methods:
        get: Retrieves the list of mushrooms.
        post: Creates a new mushroom entry.
    """
    queryset = Mushroom.objects.all()
    serializer_class = MushroomSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to retrieve mushroom list.

        Args:
            request (HttpRequest): The request object.

        Returns:
            Response: The response containing the list of mushrooms.
        """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to create a new mushroom.

        Args:
            request (HttpRequest): The request object.

        Returns:
            Response: The response containing the created mushroom data.
        """
        return self.create(request, *args, **kwargs)


class Families(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    """
    API view to retrieve list of families or create a new family.

    Methods:
        get: Retrieves the list of families.
        post: Creates a new family entry.
    """
    queryset = Family.objects.all()
    serializer_class = FamilySerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to retrieve family list.

        Args:
            request (HttpRequest): The request object.

        Returns:
            Response: The response containing the list of families.
        """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to create a new family.

        Args:
            request (HttpRequest): The request object.

        Returns:
            Response: The response containing the created family data.
        """
        return self.create(request, *args, **kwargs)


class Recipes(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    """
    API view to retrieve list of recipes or create a new recipe.

    Methods:
        get: Retrieves the list of recipes.
        post: Creates a new recipe entry.
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to retrieve recipe list.

        Args:
            request (HttpRequest): The request object.

        Returns:
            Response: The response containing the list of recipes.
        """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to create a new recipe.

        Args:
            request (HttpRequest): The request object.

        Returns:
            Response: The response containing the created recipe data.
        """
        return self.create(request, *args, **kwargs)


class Findings(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    """
    API view to retrieve list of findings or create a new finding.

    Methods:
        get: Retrieves the list of findings.
        post: Creates a new finding entry.
    """
    queryset = Finding.objects.all()
    serializer_class = FindingSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to retrieve finding list.

        Args:
            request (HttpRequest): The request object.

        Returns:
            Response: The response containing the list of findings.
        """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to create a new finding.

        Args:
            request (HttpRequest): The request object.

        Returns:
            Response: The response containing the created finding data.
        """
        return self.create(request, *args, **kwargs)


class Habitats(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    """
    API view to retrieve list of habitats or create a new habitat.

    Methods:
        get: Retrieves the list of habitats.
        post: Creates a new habitat entry.
    """
    queryset = Habitat.objects.all()
    serializer_class = HabitatSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to retrieve habitat list.

        Args:
            request (HttpRequest): The request object.

        Returns:
            Response: The response containing the list of habitats.
        """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to create a new habitat.

        Args:
            request (HttpRequest): The request object.

        Returns:
            Response: The response containing the created habitat data.
        """
        return self.create(request, *args, **kwargs)


class Profiles(mixins.ListModelMixin, generics.GenericAPIView):
    """
    API view to retrieve list of profiles.

    Methods:
        get: Retrieves the list of profiles.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to retrieve profile list.

        Args:
            request (HttpRequest): The request object.

        Returns:
            Response: The response containing the list of profiles.
        """
        return self.list(request, *args, **kwargs)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    API view to handle user login and return authentication token.

    Methods:
        post: Authenticates the user and returns a token.
    """
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key})
