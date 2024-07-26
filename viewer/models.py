from decimal import Decimal
from django.contrib.auth.models import User
from django.db import models
from accounts.models import Profile


class Family(models.Model):
    """Model representing a mushroom family."""
    name = models.CharField(max_length=100)
    name_latin = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Families"

    def __str__(self):
        return self.name


class Habitat(models.Model):
    """Model representing a habitat of a mushroom."""
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Mushroom(models.Model):
    """Model representing a mushroom."""
    EDIBILITY_CHOICES = [
        ('jedla', 'Jedlá'),
        ('nejedla', 'Nejedlá'),
        ('jedovata', 'Jedovatá'),
    ]
    name_cz = models.CharField(max_length=100)
    name_latin = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    edibility = models.CharField(max_length=10, choices=EDIBILITY_CHOICES, default='inedible')
    habitats = models.ManyToManyField(Habitat, related_name='mushrooms')
    image = models.ImageField(upload_to='mushroom_images/', null=True, blank=True)
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='mushrooms', null=True, blank=True)

    class Meta:
        ordering = ['name_cz']

    def __str__(self):
        return f"{self.name_cz} ({self.name_latin}) - {self.get_edibility_display()}"


class Finding(models.Model):
    """Model representing a finding of a mushroom."""
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='findings')
    mushroom = models.ForeignKey(Mushroom, on_delete=models.CASCADE, related_name='findings')
    description = models.TextField(null=True, blank=True)
    date_found = models.DateField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    image = models.ImageField(upload_to='finding_images/', null=True, blank=True)

    def __str__(self):
        return f"Finding of {self.mushroom.name_cz} by {self.user.user.username}"


class Recipe(models.Model):
    """Model representing a mushroom recipe."""
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='recipes')
    title = models.CharField(max_length=120)
    ingredients = models.TextField()
    instructions = models.TextField()
    image = models.ImageField(upload_to='recipe_images/', null=True, blank=True)
    main_mushroom = models.ForeignKey(Mushroom, on_delete=models.CASCADE, related_name='recipes', null=True, blank=True)
    source = models.CharField(max_length=200, null=True, blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def update_average_rating(self):
        """Updates the average rating of the recipe based on user ratings."""
        ratings = Rating.objects.filter(recipe=self)
        if ratings.exists():
            total_rating = sum(rating.hodnoceni for rating in ratings)
            average_rating = total_rating / ratings.count()
            self.rating = round(Decimal(average_rating), 1)  # round to one decimal place
        else:
            self.rating = Decimal('0.0')
        self.save()

    def num_ratings(self):
        """Returns the number of ratings for the recipe."""
        return Rating.objects.filter(recipe=self).count()


class Rating(models.Model):
    """Model representing a rating of a recipe."""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='hodnoceni')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hodnoceni = models.IntegerField(default=1, choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))

    def __str__(self):
        return f"{self.recipe.title} - {self.user.username}"


class Tip(models.Model):
    """Model representing a tip or trick."""
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='tip', null=True, blank=True)
    title = models.CharField(max_length=500)
    content = models.TextField()
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='recipe_images/', null=True, blank=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Model representing a comment on a finding."""
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    finding = models.ForeignKey(Finding, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    new = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.user.user.username} on {self.finding}"


class Message(models.Model):
    """Model representing a message."""
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} at {self.timestamp}"


class CommentRecipe(models.Model):
    """Model representing a comment on a recipe."""
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments_recipe')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    image = models.ImageField(upload_to='comments_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    new = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.user.user.username} on {self.recipe}"
