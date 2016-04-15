from django.shortcuts import render
from django.shortcuts import render
from django.template import Context, loader
from django.http import HttpResponse
from django.conf import settings
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.views.generic import UpdateView
from django import forms

from clarifai2 import clarifai

import base64
import os, requests, json, os.path
import httplib2
import smtplib
import urllib2

api = clarifai.ApiClient(base_url='api2-prod.clarifai.com',
                         client_id='<>',
                         client_secret='<>')
# filename = "all_the_pokemon"
# file = open(filename, 'r')
# arr = file.readlines()
# arr = map(lambda s: s.strip(), arr)
# for pokemon in arr:
# 	api.postImage(clarifai.Image(url=pokemon))
# 	print "DONE: ", pokemon
# file.close()

class URLForm(forms.Form):
	query = forms.CharField()

class ProfileForm(forms.Form):
	user = forms.CharField()

class LandingPageView(TemplateView):
	template_name = 'index.html'

	def get(self, request, *args, **kwargs):
		template = loader.get_template('index.html')
		context = Context({'pokemon': 'Welcome to the Pokedex','height': "Search for a pokemon", 'poke_type': 'Powered by Clarifai'})
		return HttpResponse(template.render(context))

class ResultPageView(FormView):
	template_name="index.html"
	form_class = URLForm
	success_url = '/result/'

	def get(self, request, *args, **kwargs):
		query = request.GET.get('url')
		result = api.searchImages(clarifai.Image(url=query), per_page=10)
		image = result[0]['url']
		#get poke number
		x = image[46:len(image)]
		temp = x.rpartition('/')[2]
		number = temp[0:4]
		number = filter(lambda x: x.isdigit(), number)
		print number

		info = requests.get('http://pokeapi.co/api/v2/pokemon/' + number + '/').json()
		
		name = info['name']
		ptype = ""
		for _type in info['types']:
			print _type['type']
			ptype += _type['type']['name'] + " "
		height = info['height']

		character = requests.get('http://pokeapi.co/api/v2/characteristic/' + number + "/").json()
		descriptions = character['descriptions']
		description = ""
		for des in descriptions:
			description = des['description'] + " "

		height_info = "Height: " + str(height) + " ft"
		description = "Description: " + description
		template = loader.get_template('index.html')
		context = Context({'pokemon': name.capitalize(), 'poke_image': image, 'height': height_info, 
			'description': description, 'poke_type': ptype.capitalize()})
		return HttpResponse(template.render(context))


