from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view

from realestate_api import rating as r


from django.core.cache import cache
from django.shortcuts import render


import requests
import json
import random
import pdb


MAPS_API_KEY = 'AIzaSyDBs7baI6Lq4B2A5sDtVVoFyhPOP6VBXLY'
random.seed()


#Function to get and  filter the immobilia
@api_view(['GET'])
def get_realestates(request, format=None):

    params = {

        "action" : "search_listings",
        "encoding" : "json",
        "place_name" : "germany",
        "price_max" : int(request.GET["equity"])*10,

    }


    if("number_of_results" in request.GET):
        params["number_of_results"] = request.GET["number_of_results"]
    else:
        params["number_of_results"] = 50


#    for key, value in request.GET.items():
#        params[key] = value


    #Call to the astoria API
    response = requests.get("http://api.nestoria.de/api?", params = params)

    #Analyse the data
    d = json.loads(response.text)
    dd = r.format_response(d["response"])

    top_5 = r.rate(dd["listings"])
    top_other = r.other_options(params)
    #investment_packages = r.create_packages(top_5.extend(top_other), params["price_max"])

    d = {}
    d["best_picks"] = top_5
    d["other_options"] = top_other
    #d["packages"] = investment_packages
    return Response(d)




#Testing function
@api_view(['GET'])
def test(request, format=None):
    return Response("Alles in Ordnung!")



#Function fro getting street view from cache
@api_view(['GET'])
def get_streetview(request, format=None):

    key = request.GET["key"]
    print("This is the key: " + key)

    img = cache.get(key)

    print("And this is the image: " + str(img))
    
    return Response(img)



@api_view(['GET'])
def get_map(request):

    return render(request, "map.html", {})
