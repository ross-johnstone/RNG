#IMPORTS
from django.db import models
from django.db.models import Avg
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

class UserProfile(AbstractUser):
    # AbstractUser relevant fields:
    # username, password, first_name, last_name, date_joined, email, last_login

    # boolean critic field - if true the user is set as a critic
    critic = models.BooleanField(default=False)
    website = models.URLField(null=True, blank=True)
    picture = models.ImageField(upload_to='profile_images', null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    slug = models.SlugField(max_length=40)

    def save(self, *args, **kwargs):
        self.slug=slugify(self.username)
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=64)
    # supercategory to allow hierarchical structure of categories
    supercategory = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    imageUrl= models.CharField(max_length=128, blank=True, null=True)
    slug = models.SlugField(max_length=40)

    # function to save category
    def save(self, *args, **kwargs):
        self.slug=slugify(self.name)
        super(Category,self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural='Categories'

class Game(models.Model):
    name = models.CharField(max_length=64)
    age_rating = models.CharField(max_length=16)
    description = models.CharField(max_length=9999)
    release_date = models.DateField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    picture = models.ImageField(upload_to='game_images', blank=True, null=True)
    file_name = models.CharField(max_length=32, blank=True, null=True)

    # when requesting to add a game the game must be verified by an admin
    is_approved = models.BooleanField(default=False)

    slug = models.SlugField(max_length=40)

    # aggregrate function in order to calculate normal user average rating
    @property
    def avg_user_rating(self):
        return Rating.objects.filter(game=self, critic_rating = False).aggregate(Avg('score'))

    # aggregrate function in order to calculate critic average rating
    @property
    def avg_critic_rating(self):
        return Rating.objects.filter(game=self, critic_rating = True).aggregate(Avg('score'))

    # aggregrate function for an overall average rating (including both users and critics)
    @property
    def avg_rating(self):
        return Rating.objects.filter(game=self).aggregate(Avg('score'))

    # saves the rating
    def save(self, *args, **kwargs):
        self.slug=slugify(self.name)
        super(Game, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Rating(models.Model):
    score = models.IntegerField(validators=[MaxValueValidator(10), MinValueValidator(1)])
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    # boolean field to recognise if critic/normal rating
    critic_rating = models.BooleanField(default=False)
    # links to games
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now, blank=True, null=True)

    class Meta:
        # ensure only one rating per game per user
        unique_together = ('user', 'game',)


class Comment(models.Model):
    # links to both game(in which the commnent is for) and user(who makes the comment)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    # max length set at 2000 characters
    content = models.CharField(max_length=2000)
    # includes a time stamp
    timestamp = models.DateTimeField(default=timezone.now, blank=True, null=True)

    def __str__(self):
        return '{} - {}'.format(self.game.name, str(self.user.username))