#IMPORTS
from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
import random

from RNG.models import Category, Game, Comment, Rating
from RNG.forms import CategoryForm, UserForm, GameForm, UserProfileForm, CommentForm, RatingForm

#view for home page
def index(request):
	#populates list of new and popular games
	#to display on carousels on index
	game_dict={}
	newGameList= Game.objects.order_by("-release_date")#newgames
	popGameList= Game.objects.order_by("rating")#popular games
	for popGame in popGameList:
		avg = popGame.avg_rating['score__avg']
		if avg == None:
			game_dict[popGame] = 0.0
		else:
			game_dict[popGame] = avg
	sortedPop = sorted(game_dict, key=lambda i: float(game_dict[i]))
	mostPop = sortedPop[::-1]
	topSix = mostPop[:6]
	top = topSix[0]
	topFive = topSix[1:6]
	#topFive.pop(topFive[0])
	random_index = random.randrange(0, len(popGameList))
	random_game = popGameList[random_index]
	random_cat = random_game.category
	newGames= []
	popularGames= []
	for r in newGameList:
		print(r.name, r.release_date)
        
	for i in range(1,6):
		newGames.append(newGameList[i])
		popularGames.append(popGameList[i])
    
	context_dict={"newGames":newGames,
                  "popularGames": popularGames,
				  "random_game": random_game,
				  "random_cat": random_cat,
				  "topFive": topFive,
				  "top": top}
	return render(request, 'RNG/index.html', context=context_dict)

#view for about page
def about(request):
    context_dict={}
    return render(request, 'RNG/about.html', context=context_dict)

#view for signup page
def signup(request):
	registered = False
	
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)
		
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()
			
			profile = profile_form.save(commit=False)
			profile.user = user
			
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']
				
			profile.save()
			
			registered = True
		else:
			print(user_form.errors, profile_form.errors)
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()
		
	return render(request,
				'RNG/signup.html',
				{'user_form': user_form,
				'profile_form': profile_form,
				'registered': registered})

#view for login				
def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		
		user = authenticate(username=username, password=password)
		
		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(reverse('index'))
			else:
				return HttpResponse("Your RNG account is disabled.")
		else:
			print("Invalid login details: {0}, {1}".format(username, password))
			return HttpResponse("Invalid login details supplied.")
			
	else:
		return render(request, 'RNG/signin.html', {})

#view for logout		
@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))

#view for all categories: shows all categories sorted by name	
def show_categories(request):
	context_dict={}
	try:
		categorylist = []
		categorylist=Category.objects.order_by('name')
		context_dict['category']=categorylist
	except Category.DoesNotExist:
		context_dict['category']=None
	return render(request, 'RNG/show_categories.html', context_dict)

#view for inside category: shows all games within category
def category(request, category_name_slug):
	context_dict={}
	try:
		category=Category.objects.get(slug=category_name_slug)
		games = Game.objects.filter(category=category, is_approved=True)
		context_dict['games']=games
		context_dict['category']=category
	except Category.DoesNotExist:
		context_dict['category']=None
		context_dict['games']=None
	return render(request, 'RNG/category.html', context_dict)

#view for a game page	
def gameV(request, category_name_slug, game_name_slug):
	game = Game.objects.get(slug=game_name_slug)
	current_user = request.user
	critic_score = False
	av_critic = game.avg_critic_rating['score__avg']
	av_user = game.avg_user_rating['score__avg']
	if current_user.is_authenticated:
		if current_user.critic == True:
			critic_score = True
	
	comments = Comment.objects.filter(game=game).order_by('-timestamp')
	rated = False
	ratings = Rating.objects.filter(game=game)
	for rater in ratings:
		if rater.user == request.user:
			rated = True
				
	if request.method == 'POST':
		comment_form = CommentForm(request.POST or None)
		rating_form = RatingForm(request.POST or None)
		if comment_form.is_valid():
			content = request.POST.get('content')
			comment = Comment.objects.create(game=game, user=request.user, content=content)
			comment.save()
		if rating_form.is_valid():
			score = request.POST.get('score')
				
			if critic_score:
				rating = Rating.objects.create(game=game, user=request.user, score=score, critic_rating = True)
				av_critic = game.avg_critic_rating['score__avg']
			else:
				rating = Rating.objects.create(game=game, user=request.user, score=score)
				av_user = game.avg_user_rating['score__avg']
				
			rating.save()
			rated = True
	else:
		comment_form = CommentForm()
		rating_form = RatingForm()
		
	
	context_dict = {}
	if av_critic == None:
		context_dict['av_critic'] = av_critic
	else:
		context_dict['av_critic'] = "%.2f" % round(av_critic,2)
	if av_user == None:
		context_dict['av_user'] = av_user
	else:
		context_dict['av_user'] = "%.2f" % round(av_user,2)
		
	context_dict['game']=game
	context_dict['comments']=comments
	context_dict['comment_form']=comment_form
	context_dict['rating_form']=rating_form
	context_dict['rated']=rated
	
	return render(request, 'RNG/game.html', context=context_dict)

#view for adding game	
def add_gameV(request):
	if request.method == 'POST':
		game_form = GameForm(data=request.POST)
		
		if game_form.is_valid():
			game = game_form.save()
			game.save()

			if 'picture' in request.FILES:
				game.picture = request.FILES['picture']
			game.save()
			
		else:
			print(game_form.errors)
	else:
		game_form = GameForm()
		
			
			
	context_dict={'game_form':game_form}
	return render(request, "RNG/add_game.html", context_dict)

#view for games: shows all games in library
def allgames(request):
    games= Game.objects.order_by("name")
    context_dict={"games":games}
    return render(request, 'RNG/games.html', context=context_dict)

#view for search: when using site search
def search(request):
    if request.method == 'GET':
        game_name = request.GET.get('search')
        try:
            games = Game.objects.filter(name__icontains=game_name)
        except:
            games =[]
        try:
            cats= Category.objects.filter(name__icontains=game_name)
        except:
            cats=[]
        return render(request, "RNG/games.html", {"games": games, "cats": cats})
    else:
        return render(request, "RNG/games.html", {})
