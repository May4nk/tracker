from rest_framework.serializers import ModelSerializer

from .models import Candidate

class CandidateSerializer(ModelSerializer):
	class Meta:
		model = Candidate
		fields = [
			"id",
			"name",
			"email",
			"age",
			"gender",
			"phone_number",
			"status"
		]