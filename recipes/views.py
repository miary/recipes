import os, time, re
from django.shortcuts import render
from .models import Recipe
from recipes.ingredientsForm import IngredForm
from django.shortcuts import render, redirect
#from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
from dotenv import load_dotenv
import openai


load_dotenv() 
openai.api_key = os.getenv("OPENAI_API_KEY")
llm_model = os.getenv("LLM_MODEL_RECIPE", "gpt-4")

def index(request):
    context = {"ingform": IngredForm()}
    return render(request, 'index.html', context)


# Use data from form to query recipes through LLM
def query_recipes(staple, main, leaves, meat, request):
    leaves = ""

    prompt = (f"You are a chef who is an expert in African cuisine and knowlegable about African recipes.\n" 
        f"List in a bullet point form at list three African recipes that must contain the following ingredients:\n" 
        f"Add the following leaves to the ingredidents: {leaves}.\n"
        f" {staple} , {main}, mixed only with the following type of meat: {meat}.\n" 
        f"Use exclusively the meat provided and do not include recipes that have other types of meat from the list. " 
        f"Be thorough and make sure that the recipes contain all the necessary ingredients as well as the " 
        f"detailed steps and necessary preparation before starting the cooking.\n" 
        f"Whenever possible provide also information about cooking time.\n"
        f"Format and outputyour response as a python list")
    try:
        completion = openai.ChatCompletion.create(
            model=llm_model,
            temperature=0,
            messages=[{"role":"assistant", "content": prompt}],
            max_tokens=3000,
        )
    except openai.APIError as e:
        # Handle API errors here
        return "An error occurred while processing Openai API request: {}".format(e)

    # Get the response text from the ChatGPT API
    message = completion.choices[0].message.content
    #messages.success(request, 'Recipes successfully retrieved.')

    formatted = formatResponse(message)
    
    return formatted


def formatResponse(response):
    recList = []
    matched = re.finditer("\d[.]", response)
    first = 0
    for m in matched:
        if first == 0:
            first = first+1
            recList += [response[0:m.start()]]
            next = m.start()
        else:
            recList += [response[next:m.start()]]
            next = m.start()

    leng = len(response)
    recList += [response[next:leng]]
    return(recList)

    
def ingredDisplay(request):
    selected_main = "" 
    selected_staple = ""
    selected_leaves = ""
    selected_meat = ""
    
    formdata = request.POST

    selected_main = formdata.get('main')
    selected_staple = formdata.get('staple')
    selected_leaves = formdata.get('leaves')
    selected_meat = formdata.get('meat')
    
    llm_response = query_recipes(selected_main, selected_staple, selected_leaves, selected_meat, request)
    
    return render(request, 'response.html', {'llm_response': llm_response})
   
