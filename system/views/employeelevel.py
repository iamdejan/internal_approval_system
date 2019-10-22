from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view

from system.models import EmployeeLevel, BaseResponse, build_success_response, build_fail_response
from system.serializers import EmployeeLevelSerializer

def save_new_level(data):
    level_name = data["level_name"]
    description = data["description"]

    new_level = EmployeeLevel(level_name = level_name, description = description)
    new_level.save()
    return new_level

def update_level(id, data):
    id = int(id)
    level_name = data["level_name"]
    description = data["description"]
    EmployeeLevel.objects.filter(id = id).update(level_name = level_name, description = description)

@api_view(["GET"])
def levels(request):
    levels = EmployeeLevel.objects.all()
    serializer = EmployeeLevelSerializer(levels, many = True)

    response = build_success_response(serializer.data)
    return JsonResponse(response.serialize(), safe = False)

@api_view(["POST"])
def add_level(request):
    data = request.data
    new_level = save_new_level(data)
    serializer = EmployeeLevelSerializer(new_level)

    response = build_success_response(serializer.data)
    return JsonResponse(response.serialize(), safe = False)

@api_view(["GET"])
def get_level(request, id):
    id = int(id)
    try:
        employee_level = EmployeeLevel.objects.get(id = id)
        serializer = EmployeeLevelSerializer(employee_level)

        response = build_success_response(serializer.data)
        return JsonResponse(response.serialize(), safe = False)
    except:
        response = build_fail_response({
            "message": "NOT_FOUND"
        })
        response = JsonResponse(response.serialize(), safe = False)
        response.status_code = 404
        return response

@api_view(["PUT"])
def update_employee_level(request, id):
    id = int(id)
    update_level(id, request.data)

    employee_level = EmployeeLevel.objects.get(id = id)
    serializer = EmployeeLevelSerializer(employee_level)

    response = build_success_response(serializer.data)
    return JsonResponse(response.serialize(), safe = False)

@api_view(["DELETE"])
def delete_level(request, id):
    EmployeeLevel.objects.filter(id = id).delete()

    response = build_success_response({})
    return JsonResponse(response.serialize(), safe = False)