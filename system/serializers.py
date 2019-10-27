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
        fields = ["id", "first_name", "last_name", "level_id"]

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "title", "checklist_mask", "tail_hash"]

class ApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Approval
        fields = ["hash", "project_id", "employee_id", "previous_hash"]

class SmartContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmartContract
        fields = ["contract_code", "threshold", "description"]