from rest_framework import fields, serializers
from rest_framework.serializers import ModelSerializer
from master.models import Bdlreimbursement


class DetailLogbookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bdlreimbursement
        fields = ('id','doc_id', 'budget_code', 'bdldate','start_km','finish_km','km','curr','bdl_perkm','bdl_amount','bdl_total','destinationfrom','destinationto','purpose','parking','toll','policeno','carbrand','cartype','tips','bensin')