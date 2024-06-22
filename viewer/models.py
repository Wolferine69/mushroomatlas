from django.db import models

from accounts.models import Profile


# Create your models here.
class Family(models.Model):
    name = models.CharField(max_length=100)
    name_latin = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Mushroom(models.Model):
    """Model representing a mushroom family."""
    EDIBILITY_CHOICES = [
        ('jedla', 'Jedlá'),
        ('nejedla', 'Nejedlá'),
        ('jedovata', 'Jedovatá'),
    ]
    HABITAT_CHOICES = [
        ('listnaty', 'Listnatý les'),
        ('jehlicnaty', 'Jehličnatý les'),
        ('smiseny', 'Smíšený les'),
        ('louka', 'Louka'),
        ('jine', 'Jiné'),
    ]
    name_cz = models.CharField(max_length=100)
    name_latin = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    edibility = models.CharField(max_length=10, choices=EDIBILITY_CHOICES, default='inedible', )
    habitat = models.CharField(max_length=10, choices=HABITAT_CHOICES, default='mixed', )
    image = models.ImageField(upload_to='mushroom_images/', null=True, blank=True)
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='mushrooms', null=True, blank=True)

    def __str__(self):
        return f"{self.name_cz} ({self.name_latin}) - {self.get_edibility_display()} - Habitat: {self.get_habitat_display()}"


class Finding(models.Model):
    """Model representing a finding of a mushroom."""
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='findings')
    mushroom = models.ForeignKey(Mushroom, on_delete=models.CASCADE, related_name='findings')
    description = models.TextField(null=True, blank=True)
    date_found = models.DateField()
    location = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='finding_images/', null=True, blank=True)

    def __str__(self):
        return f"Finding of {self.mushroom.name_cz} by {self.user.username}"


class Recipe(models.Model):
    """Model representing a mushroom recipe."""
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='recipes')
    title = models.CharField(max_length=100)
    ingredients = models.TextField()
    instructions = models.TextField()
    image = models.ImageField(upload_to='recipe_images/', null=True, blank=True)
    main_mushroom = models.ForeignKey(Mushroom, on_delete=models.CASCADE, related_name='recipes', null=True, blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Model representing a comment on a finding."""
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    finding = models.ForeignKey(Finding, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.finding}"
