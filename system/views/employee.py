from django.http import JsonResponse

from rest_framework.decorators import api_view

from system.models import Employee, BaseResponse, build_success_response, build_fail_response
from system.serializers import EmployeeSerializer

def build_new_employee(data):
    first_name = data["first_name"]
    last_name = data["last_name"]
    username = data["username"]
    level_id = int(data["level_id"])
    password = data["password"]

    employee = Employee(
        first_name = first_name,
        last_name = last_name,
        username = username,
        level_id = level_id,
    )
    employee.set_password(password)
    employee.save()
    return employee

@api_view(["GET"])
def get_all_employees(request):
    employees = Employee.objects.all()
    serializer = EmployeeSerializer(employees, many = True)

    response = build_success_response(serializer.data)
    return JsonResponse(response.serialize(), safe = False)

"""
Example request:
{
	"first_name": "Super",
	"last_name": "User",
	"username": "superuser",
	"level_id": 5,
	"password": "xxx"
}
"""
@api_view(["POST"])
def add_employee(request):
    data = request.data
    employee = build_new_employee(data)
    serializer = EmployeeSerializer(employee)

    response = build_success_response(serializer.data)
    return JsonResponse(response.serialize(), safe = False)

@api_view(["GET"])
def get_employee(request, id):
    id = int(id)
    try:
        employee = Employee.objects.get(id = id)
        serializer = EmployeeSerializer(employee)

        response = build_success_response(serializer.data)
        return JsonResponse(response.serialize(), safe = False)
    except:
        response = build_fail_response({
            "message": "NOT_FOUND"
        })
        response = JsonResponse(response.serialize(), safe = False)
        response.status_code = 404
        return response

"""
Example request:
{
	"first_name": "Giovanni",
	"last_name": "Dejan",
	"username": "iamdejan",
	"level_id": 1,
}
"""
@api_view(["PUT"])
def update_employee(request, id):
    id = int(id)

    data = request.data
    first_name = data["first_name"]
    last_name = data["last_name"]
    username = data["username"]
    level_id = data["level_id"]
    employee = Employee.objects.filter(id = id).update(
        first_name = first_name,
        last_name = last_name,
        username = username,
        level_id = level_id,
    )

    employee = Employee.objects.get(id = id)
    serializer = EmployeeSerializer(employee)

    response = build_success_response(serializer.data)
    return JsonResponse(response.serialize(), safe = False)

"""
Example request (x-www-form-urlencoded):
Key: public_key
Value: (as follows)
-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAo2L09OJNA1NU/Tj8rNMN
hw3FQKm/oGOW9mTi5DfRLcQfPwTBUS9BE2WFHUdqfL+9ISeDsFbjxqZGEm7QATvs
letqrkPacGRjZTHkz5EMoQwNvXAFrB48uB87abhtvDRBScOkG4PmlEw6z477wriU
OiBdL0q3csUa2/Dwx0I6tN62OlL0LqucKaXG/pOsV20JzvRm6nWVh1Jn6n3gbrJC
NaRWu3FenpmC/eH4r6Uvy3SJJ/mn67XNunsdUzwZiQfHe6GeLsafWceOh7PQDj4L
8WQ0L+Z+s3nzm1K2fXA83DaEVOC4sI5QwrwFx7ryPD/bDmEp7a5lz1j7wHfNJCjN
/C5aoUHFwlKCOX6SorjdVUCx0Mq7bIOMbiv1/SkUPH9ltbq8M9kMM/liLPPYl5D+
fQ2NlEzDw8x0IAfRBC849JUGA73ywBSy2M57G41IlVK5zYecFfBJVtmJwvncQEa7
eyN8VCT1WBRjl7TsQWC2mkTjzAOcx1hpTHAAZ/bSUnCeV3nSxlC6YthjDk30sQEH
swHLWmZitKKcmmWSi21UuQFSi64FEH8f9DB8u9ZZinCyH+gBp9hKXHnz32/0m8Uz
F9ObLo8ML49ngdABjAj+vOd7qsy0kuVO1uM2S7rrMCWjdWZquOmKLJLog8c7kbAV
WYS2bIZ79KastX8OSTO0hccCAwEAAQ==
-----END PUBLIC KEY-----
"""
@api_view(["PUT"])
def update_public_key(request, id):
    id = int(id)
    public_key = request.data["public_key"]
    Employee.objects.filter(id = id).update(
        public_key = public_key
    )

    response = build_success_response({
        "id": id,
    })
    return JsonResponse(response.serialize(), safe = False)

@api_view(["DELETE"])
def delete_employee(request, id):
    id = int(id)
    Employee.objects.filter(id = id).delete()

    response = build_success_response({})
    return JsonResponse(response.serialize(), safe = False)