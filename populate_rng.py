import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','RNG_project.settings')
import django
django.setup()
from RNG.models import Category, Game, Rating, UserProfile, Comment

import random
from string import ascii_lowercase  # for generating strings
from django.utils.dateparse import parse_date   # string to datetime
from django.db import IntegrityError    # catch unique constraint

action = [
    {"name": "Assassin's Creed 2",
     "user_score": 4,
     "num_user_ratings": 5,
     "critic_score": 5,
     "num_critic_ratings": 5,
     "age_rating": 18,
     "description": "An action adventure game focussed on the story of Ezio Auditore da Firenze, an assassin, in Renaissance Italy.",
     "release_date": "2009-11-17",
     "picture": "ac2.jpg",
     "file_name": "ac2.jpg"},
    {"name": "Grand Theft Auto V",
     "user_score": 3,
     "num_user_ratings": 5,
     "critic_score": 5,
     "num_critic_ratings": 5,
     "age_rating": 18,
     "description": "An open-world action game focussing on the lives of three criminals residing in Los Santos.",
     "release_date": "2013-09-17",
     "picture": "gtav.jpg",
     "file_name": "gtav.jpg"},
    {"id": "DISH",
     "name": "Dishonored",
     "user_score": 5,
     "num_user_ratings": 5,
     "critic_score": 5,
     "num_critic_ratings": 5,
     "age_rating": 18,
     "description": "An action adventure game set in an alternate dystopian Victorian England reality in which a bodyguard turned assassin seeks revenge on those who conspired against him.",
     "release_date": "2012-10-09",
     "picture": "dish.jpg",
     "file_name": "dish.jpg"}
]
rpg = [
    {"name": "Skyrim",
     "user_score": 5,
     "num_user_ratings": 5,
     "critic_score": 5,
     "num_critic_ratings": 5,
     "age_rating": 15,
     "description": "An open-world role playing game set in the fictional world of Skyrim where dragons have mysteriously reappeared.",
     "release_date": "2011-11-11",
     "picture": "sky.jpg",
     "file_name": "sky.jpg"},
    {"name": "Mass Effect 2",
     "user_score": 1,
     "num_user_ratings": 5,
     "critic_score": 5,
     "num_critic_ratings": 5,
     "age_rating": 15,
     "description": "An open-world role playing game set far in the future where faster than light travel is common technology. Commander Shepard must face many enemies and moral dilemmas in his fight against the Collectors.",
     "release_date": "2010-01-26",
     "picture": "me2.jpg",
     "file_name": "me2.jpg"},
    {"id": "DAI",
     "name": "Dragon Age: Inquisition",
     "user_score": 2,
     "num_user_ratings": 5,
     "critic_score": 5,
     "num_critic_ratings": 5,
     "age_rating": 18,
     "description": "An open-world role playing game set in a demon-filled medieval world. The only way to save the world is to recreate the long forgotten inquisition.",
     "picture": "dai.jpg",
     "file_name": "dai.jpg",
     "release_date": "2014-11-18"}
]
strategy = [
    {"name": "DOTA 2",
     "user_score": 0,
     "num_user_ratings": 5,
     "critic_score": 5,
     "num_critic_ratings": 5,
     "age_rating": 16,
     "description": "A strategy game in which you have a selection of heroes, each taking hours to master, and fight in a team of six against the other team.",
     "picture": "dota2.jpg",
     "file_name": "dota2.jpg",
     "release_date": "2013-07-09"},
    {"name": "Civilization V",
     "user_score": 3,
     "num_user_ratings": 5,
     "critic_score": 5,
     "num_critic_ratings": 5,
     "age_rating": 12,
     "description": "A strategy game in which you create a civilization and develop it over millenia amongst other civilizations all aiming for victory.",
     "picture": "civ5.jpg",
     "file_name": "civ5.jpg",
     "release_date": "2010-09-21"},
    {"name": "Spore",
     "user_score": 1,
     "num_user_ratings": 5,
     "critic_score": 5,
     "num_critic_ratings": 5,
     "age_rating": 12,
     "description": "A strategy game in which you create a single-celled organism that evolves over millenia into the world's dominant species.",
     "picture": "spore.jpg",
     "file_name": "spore.jpg",
     "release_date": "2008-09-04"}
]
puzzle = [
    {"name": "Portal 2",
     "user_score": 4,
     "num_user_ratings": 5,
     "critic_score": 5,
     "num_critic_ratings": 5,
     "age_rating": 12,
     "description": "A singleplayer/multiplayer puzzle game revolving around the use of a portal gun. Set in an abandoned laboratory populated by yourself and AI's.",
     "picture": "portal2.jpg",
     "file_name": "portal2.jpg",
     "release_date": "2011-04-18"},
    {"name": "The Talos Principle",
     "user_score": 3,
     "num_user_ratings": 5,
     "critic_score": 5,
     "num_critic_ratings": 5,
     "age_rating": 12,
     "description": "A singleplayer puzzle game set in an empty robot-filled world.",
     "picture": "ttp.jpg",
     "file_name": "ttp.jpg",
     "release_date": "2014-12-11"},
    {"name": "The Witness",
     "user_score": 0,
     "num_user_ratings": 5,
     "critic_score": 5,
     "num_critic_ratings": 5,
     "age_rating": 12,
     "description": "A singleplayer puzzle game set on a mysterious island.",
     "picture": "thewitness.jpg",
     "file_name": "thewitness.jpg",
     "release_date": "2016-01-26"}
]
sports = [
    {"name": "Rocket League",
     "user_score": 1,
     "num_user_ratings": 5,
     "critic_score": 5,
     "num_critic_ratings": 5,
     "age_rating": 3,
     "description": "A sports game resembling football only with cars and exploding goals.",
     "picture": "rocketleague.jpg",
     "file_name": "rocketleague.jpg",
     "release_date": "2015-07-07"},
    {"name": "Fifa 19",
     "user_score": 0,
     "num_user_ratings": 5,
     "critic_score": 5,
     "num_critic_ratings": 5,
     "age_rating": 3,
     "description": "A sports game allowing you to take control in your very own footballing world.",
     "picture": "fifa19.jpg",
     "file_name": "fifa19.jpg",
     "release_date": "2018-09-28"},
    {"name": "NBA 2K19",
     "user_score": 3,
     "num_user_ratings": 5,
     "critic_score": 5,
     "num_critic_ratings": 5,
     "age_rating": 3,
     "description": "A sports game allowing you to take control in your very own basketballing world.",
     "picture": "nba2k19.jpg",
     "file_name": "nba2k19.jpg",
     "release_date": "2018-09-07"}
]
mmo = [
    {"name": "World Of Warcraft",
     "user_score": 0,
     "num_user_ratings": 5,
     "critic_score": 5,
     "num_critic_ratings": 5,
     "age_rating": 12,
     "description": "An MMORPG featuring a huge expansive world with multiple choices for race and class along with near-infinite quests.",
     "picture": "wow.jpg",
     "file_name": "wow.jpg",
     "release_date": "2004-11-23"},
    {"name": "Elder Scrolls Online",
     "user_score": 1,
     "num_user_ratings": 5,
     "critic_score": 5,
     "num_critic_ratings": 5,
     "age_rating": 12,
     "description": "An MMORPG featuring a huge expansive world with multiple choices for race and class along with near-infinite quests set in the same universe as Skyrim.",
     "picture": "eso.jpg",
     "file_name": "eso.jpg",
     "release_date": "2014-04-04"},
    {"name": "Guild Wars 2",
     "user_score": 0,
     "num_user_ratings": 5,
     "critic_score": 5,
     "num_critic_ratings": 5,
     "age_rating": 12,
     "description": "An MMORPG featuring a huge expansive world with multiple choices for race and class along with near-infinite quests.",
     "picture": "gw2.jpg",
     "file_name": "gw2.jpg",
     "release_date": "2012-08-28"}
]
simulation = [
    {"name": "The Sims 4",
     "user_score": 2,
     "num_user_ratings": 5,
     "critic_score": 5,
     "num_critic_ratings": 5,
     "age_rating": 3,
     "description": "A simulation game in which you create an avatar and dictate it's life in the simulated world of Sims.",
     "picture": "sims4.jpg",
     "file_name": "sims4.jpg",
     "release_date": "2014-09-02"},
    {"name": "Kerbal Space Program",
     "user_score": 4,
     "num_user_ratings": 5,
     "critic_score": 5,
     "num_critic_ratings": 5,
     "age_rating": 3,
     "description": "A simulation game in which you build rockets to be piloted by strange minion-like creatures.",
     "picture": "ksp.jpg",
     "file_name": "ksp.jpg",
     "release_date": "2011-06-24"},
    {"name": "Farming Simulator 19",
     "user_score": 3,
     "num_user_ratings": 5,
     "critic_score": 5,
     "num_critic_ratings": 5,
     "age_rating": 3,
     "description": "A simulation game in which you own and manage a farm.",
     "picture": "fs19.jpg",
     "file_name": "fs19.jpg",
     "release_date": "2018-11-20"}
]

# cats={"Action":{"games":action, "reviews":0},
#     "RPG":{"games":rpg, "reviews":0},
#     "Strategy":{"games":strategy, "reviews":0},
#     "Puzzle":{"games":puzzle, "reviews":0},
#     "Sports":{"games":sports, "reviews":0},
#     "MMO":{"games":mmo, "reviews":0},
#     "Simulation":{"games":simulation, "reviews":0},
# }

# maintained dict structure here in case we want to add supercategories
cats = {"Action": action,
        "RPG": rpg,
        "Strategy": strategy,
        "Puzzle": puzzle,
        "Sports": sports,
        "MMO": mmo,
        "Simulation": simulation,
        }


def generate_string(length):
    return "".join(random.choice(ascii_lowercase) for i in range(length))

def generate_user(critic):
    username = generate_string(10)
    print(username)
    first_name = generate_string(10)
    last_name = generate_string(10)
    user = UserProfile.objects.get_or_create(username=username, first_name=first_name, last_name=last_name, critic=critic)[0]
    user.save()
    return user


def generate_user(critic):
    username = generate_string(10)
    print(username)
    first_name = generate_string(10)
    last_name = generate_string(10)
    critic=critic
    user = UserProfile.objects.get_or_create(username=username, first_name=first_name, last_name=last_name, critic=critic)[0]
    user.save()
    return user

def generate_rating(game, user, critic_rating):
    # generate random val between 1-10
    score = random.randint(1, 10)
    #critic_rating = (random.choice([True,False])==2)
    rating = Rating.objects.get_or_create(score=score, game=game, user=user, critic_rating=critic_rating)[0]
    rating.save()
    return rating


def generate_comment(game, user, comment=None):
    content = ["This game was excellent, would recommend playing", "10/10 IGN", "Stunning experience",
     "Awful experience, should not have been made", "This game lit", "It was aight", "Could have been better",
      "Am I first?", "This game is toxic", "So difficult I broke my controller", "Not bad 7/5", "This is an underrated gem",
      "It's good but it's no Witcher 3, praise Geraldo", "Controls are easy", "Good graphics", "I don't agree with any of you people",
      "Gave me a sense of pride and accomplishment", "Amazing", "Wow", "XD", "I love this game",
       "I left my wife so I could be with this game", "needs more water", "good with mods", "like skyrim but with guns",
       "Keep up the good work", "What are games?", "This game was shocking", "A fantastic experience", "Great story",
       "Amazing to think it was only made in 5 days", "Trailer was better than game", ";)", "Curse you Perry the Platypus",
       "First", "sᴉɥʇ pɐǝɹ oʇ uǝǝɹɔs ɹnoʎ uɹnʇ oʇ ǝʌɐɥ llᴉʍ noʎ os uʍop ǝpᴉsdn sᴉɥʇ ƃuᴉdʎʇ ɯɐ I"]

    comment = content[random.randint(0,len(content)-1)]
    if comment is None:
        comment = Comment.objects.get_or_create(user=user, game=game, content=comment)[0]
    else:
        comment = Comment.objects.get_or_create(user=user, game=game, content=comment)[0]
    comment.save()
    return comment

def generate_game(category, name, age_rating, release_date, is_approved, description, picture = None, file_name = None, ):
    # [0] specifies object in the [object, boolean created]
    game = Game.objects.get_or_create(category=category, name=name,
                                      age_rating=age_rating, release_date=release_date,
                                      is_approved=is_approved, picture=picture, file_name=file_name, description=description)[0]
    game.save()
    return game

def generate_category(name):
    c=Category.objects.get_or_create(name=name, imageUrl="/static/images/"+name.lower()+".jpg")[0]
    c.save()
    return c


def populate():
    # generate users
    NUM_REGULAR_USERS = 100
    NUM_CRITIC_USERS = 20
    NUM_USERS = NUM_REGULAR_USERS + NUM_CRITIC_USERS  # don't make lower than 20

    for i in range(NUM_REGULAR_USERS):
        generate_user(critic=False)
        print("Generating normal user")

    for i in range(NUM_CRITIC_USERS):
        generate_user(critic=True)
        print("Generating critic")

    users = UserProfile.objects.all()

    def get_random_user():
        return random.choice(users)

    ### MAIN POPULATE LOOP ###
    for name, games in cats.items():
        # generate categories
        print("Creating " + name + " category")
        category = generate_category(name)

        # generate games for those categories
        for game_dict in games:
            print("Creating " + game_dict["name"] + " game")
            game = generate_game(category=category, name=game_dict["name"],
                                 age_rating=game_dict["age_rating"],
                                 release_date=parse_date(game_dict["release_date"]),
                                 is_approved=True,
                                 picture=game_dict["picture"],
                                 file_name=game_dict["file_name"],
                                 description=game_dict["description"]
                                 )

            # generate ratings for game
            for i in range(random.randint(0, 20)):
                print("Creating rating")
                try:
                    rating = generate_rating(user=get_random_user(), game=game,
                                             critic_rating=random.choice([True, False]))
                    rating.save()
                except IntegrityError:  # catch unique_constraint failed
                    ...

            # generate comments for game
            num_comments = random.randint(0, 10)
            for i in range(num_comments):
                prev_comment = None

                # randomly allocate comments as subcomments
                num_sub_comments = random.randint(1, num_comments - i)
                for x in range(random.randint(1, num_sub_comments)):
                    print("Creating comment")
                    comment = generate_comment(game=game, user=get_random_user(),
                                               comment=prev_comment)
                    prev_comment = comment
                i = i + num_sub_comments


    for c in Category.objects.all():
        for p in Game.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(p)))

if __name__ == '__main__':
    print("*** Starting RNG population script ***")
    populate()
