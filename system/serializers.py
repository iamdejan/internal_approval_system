from rest_framework import serializers
from system.models import *

class BaseResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseResponse
        fields = ["success", "data"]

class EmployeeLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeLevel
        fields = ["id", "level_name", "description"]

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["id", "first_name", "last_name", "level"]

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "title"]

class ApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Approval
        fields = ["project", "data", "employee"]

class SmartContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmartContract
        fields = ["contract_code", "threshold", "description"]