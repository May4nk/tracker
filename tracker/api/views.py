from operator import add
from functools import reduce
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Q, Case, When, Value, IntegerField
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank

from .models import Candidate
from .serializers import CandidateSerializer

@api_view(["GET"])
def home(req):
	try:
		candidates = Candidate.objects.all()
	except:
		return Response({ "message": "Fetching candidates failed.." }, status=500)
	
	serialized_candidates = CandidateSerializer(candidates, many=True).data
	return Response({ "message": "All candidates fetched", "data": serialized_candidates })

@api_view(["GET"])
def fetch_candidate(req, candidate_id: int):
	try:
		candidate = Candidate.objects.get(id=candidate_id)
	except Candidate.DoesNotExist:
		return Response({ "message": "Candidate not found"}, status=404)
	
	serialized_candidate = CandidateSerializer(candidate).data
	return Response({ "message": "Candidate fetched", "data": serialized_candidate })
	

@api_view(["GET"])
def del_candidate(req, candidate_id: int):
	try:
		candidate = Candidate.objects.get(id=candidate_id)
	except Candidate.DoesNotExist:
		return Response({ "message": "Candidate not found"}, status=404)
	
	candidate.delete()
	return Response({ "message": "Candidate deleted" })
	
@api_view(["PATCH"])
def update_candidate(req, candidate_id: int):
	try: 
		candidate = Candidate.objects.get(id=candidate_id)
	except Candidate.DoesNotExist:
		return Response({ "message": "Candidate not found"}, status=404)
	
	serializer = CandidateSerializer(candidate, data=req.data[0], partial=True)
	if serializer.is_valid():
		instance = serializer.save()
		data = CandidateSerializer(instance).data
		return Response({ "message": "Candidate updated", "data": data })
	
	return Response({ "message": "Try again: Data is not valid", "error": serializer.errors }, status=500)

@api_view(["POST"])
def create_candidate(req):
	candidates_data = req.data
	print(candidates_data)
	multi_candidates = isinstance(candidates_data, list)
	serializer = CandidateSerializer(data=req.data, many=multi_candidates)

	if serializer.is_valid():
		instance = serializer.save()
		data = CandidateSerializer(instance, many=multi_candidates).data	
		return Response({ "message": "New candidates created", "data": data })
	
	return Response({ "message": "Data is not valid", "error": serializer.errors }, status=500)

@api_view(["GET"])
def search_candidate(req, candidate_name: str):
	try:
		q_filter = Q()
		annotations = []
		name_query_params = candidate_name.strip().split()

		for param in name_query_params:
			q_filter |= Q(name__icontains=param)
			annotations.append(
				Case(
					When(name__icontains=param, then=Value(1)),
					default=Value(0),
					output_field=IntegerField()
				)
       		)

		relevance_expr = reduce(add, annotations)
		candidates_found = Candidate.objects.filter(q_filter).annotate(
			relevance=relevance_expr
		).order_by("-relevance", "name")
		

		# Another approach with full text search in postgres

		# search_vector = SearchVector("name")
		# query = SearchQuery(candidate_name)
		# candidates_found = Candidate.objects.annotate( 
		# 	rank=SearchRank(search_vector, query)
		# ).filter(rank__gt=0).order_by("-rank")
	except Candidate.DoesNotExist:
		return Response({ "message": "No candidate found"}, status=404)
	
	serialized_candidates = CandidateSerializer(candidates_found, many=True).data
	return Response({ "message": "Found candidates", "data": serialized_candidates })