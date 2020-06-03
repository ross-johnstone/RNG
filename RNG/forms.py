#IMPORTS
from django import forms
from RNG.models import UserProfile, Category, Game, Comment, Rating
from django.contrib.auth.models import User
from django import forms

#form passing in variables for category view
class CategoryForm(forms.ModelForm):
	name = forms.CharField(max_length=128,
							help_text="Please enter the category name.")
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	slug = forms.CharField(widget=forms.HiddenInput(), required=False)

	class Meta:
		model = Category
		fields = ('name',)

#form passing in variables for game
class GameForm(forms.ModelForm):

	class Meta:
		model = Game
		fields = ("name", "age_rating", "description", "release_date", "category", "picture", "file_name")
	
#form passing in variables for rating
class RatingForm(forms.ModelForm):
	score = forms.FloatField()
	class Meta:
		model = Rating
		fields = ("score", )

#form passing in variables for userform
class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput()) #,max_length = 32, help_text="Create a password of at least 8 characters long ",required=True)

	class Meta:
		model = User
		fields = ("username", "email",  "password")

#form passing in variables for userprofileform (for critic users)		
class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ("website", "picture")

#form passing in variables for comments
class CommentForm(forms.ModelForm):
	#text in comment
	content=forms.CharField(label="",widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Add a public comment here','rows':'4','cols':'50'}))
	class Meta:
		model = Comment
		fields = ("content", )
