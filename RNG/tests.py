from django.test import TestCase
from RNG.models import Game, Category, UserProfile, Comment, Rating
from django.utils.dateparse import parse_date   # parse date field for game
import random
from string import ascii_lowercase  # for generating strings
from django.utils import timezone
import populate_rng

# Create your tests here.

# Run with python manage.py test RNG
class DatabaseSaveTests(TestCase):
    cat = None
    game = None
    user = None
    rating = None
    comment = None

    def generate_string(self, length):
        return "".join(random.choice(ascii_lowercase) for i in range(length))

    def generate_category(self):
        cat = populate_rng.generate_category("TestCategory")
        return cat

    def generate_game(self):
        category = self.generate_category()
        game = populate_rng.generate_game(category=category, name="TestGame",
                                          release_date=parse_date("2019-04-03"),
                                          age_rating="18", is_approved=True,
                                          description="Test description here")
        return game

    def generate_user(self):
        username = self.generate_string(10)
        first_name = self.generate_string(10)
        last_name = self.generate_string(10)

        user = UserProfile.objects.get_or_create(username=username, first_name=first_name,
                                                 last_name=last_name)[0]
        user.save()
        return user, username, first_name, last_name

    def generate_rating(self):
        game = self.generate_game()
        user = self.generate_user()[0]
        rating = populate_rng.generate_rating(game=game, user=user, critic_rating=user.critic)
        return rating, rating.score, user, game

    def generate_comment(self):
        game = self.generate_game()
        user = self.generate_user()[0]
        comment = populate_rng.generate_comment(user=user, game=game)
        return comment, game, user, comment.content


    def test_ensure_category_fields_correct(self):
        # create cat then save, test if saved correctly
        cat = self.generate_category()
        self.assertEqual((cat.name=="TestCategory"), True)

    def test_ensure_game_fields_correct(self):
        # save a game then test if the fields are correct
        # create cat first to test

        game = self.generate_game()
        cat = self.generate_category()

        self.assertEquals((game.name=="TestGame" and game.age_rating=="18" and
                           game.description=="Test description here" and
                           game.release_date==parse_date("2019-04-03") and
                           game.category==cat), True)

    def test_ensure_userprofile_fields_correct(self):
        username = self.generate_string(10)
        first_name = self.generate_string(10)
        last_name = self.generate_string(10)
        description = self.generate_string(40)

        user, username, first_name, last_name = self.generate_user()

        self.assertEquals((user.username==username and user.first_name==first_name and
                           user.last_name==last_name), True)

    def test_ensure_rating_fields_correct(self):
        rating, score, user, game = self.generate_rating()

        self.assertEquals((rating.score==score and rating.user==user and
                           rating.game==game), True)

    def test_ensure_comment_fields_correct(self):
        comment, game, user, content = self.generate_comment()

        self.assertEquals((comment.game==game and comment.user==user and comment.content==content), True)

    # test_ensure_category_fields_correct()
    # test_ensure_game_fields_correct()
    # test_ensure_userprofile_fields_correct()
    # test_ensure_rating_fields_correct()
    # test_ensure_comment_fields_correct()



