import requests
from django.shortcuts import render

url = "http://localhost:8000/api/candidate"

def home(req):
	response = requests.get(url)
	candidates = []
	if response.status_code == 200:
		candidates = response.json().get("data", [])

	return render(req, "track/home.html", { "candidates": candidates })

def candidate_page(req, user_id):
	response = requests.get(f"{url}/get/{user_id}")
	if response.status_code == 200:
		candidate = response.json().get("data")
		
	return render(req, "track/user.html", { "candidate": candidate})

# def search(req):
# 	query = req.GET.get("q", "")
# 	candidates = []

# 	if query:
# 		response = requests.get(f"http://localhost:8000/api/candidate/search/{query}")
# 		if response.status_code == 200:
# 			candidates = response.json().get("data", [])

# 	return render(req, "track/search.html", { "found_candidates": candidates, "query": query })