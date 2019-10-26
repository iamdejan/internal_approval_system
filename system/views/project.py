from django.http import JsonResponse

from rest_framework.decorators import api_view

from system.models import Approval, Project, Employee, build_fail_response, build_success_response
from system.serializers import ApprovalSerializer, ProjectSerializer

import json

NO_DATA_HASH = ''.join(["0" for i in range(128)])

@api_view(["GET"])
def get_all_projects(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many = True)

    response = build_success_response(serializer.data)
    return JsonResponse(response.serialize(), safe = False)

"""
Example request:
{
    "title": "Ultimate Scholarship"
}
"""
@api_view(["POST"])
def add_new_project(request):
    data = request.data
    project = Project(
        title = data["title"],
        checklist_mask = 0,
        head_hash = NO_DATA_HASH,
        tail_hash = NO_DATA_HASH,
    )
    project.save()
    serializer = ProjectSerializer(project)

    response = build_success_response(serializer.data)
    return JsonResponse(response.serialize(), safe = False)

@api_view(["GET"])
def get_project(request, id):
    id = int(id)

    project = Project.objects.get(id = id)
    serializer = ProjectSerializer(project)

    response = build_success_response(serializer.data)
    return JsonResponse(response.serialize(), safe = False)

@api_view(["PUT"])
def update_project(request, id):
    id = int(id)

    project = Project.objects.get(id = id)
    project.title = request.data["title"]
    project.save()
    serializer = ProjectSerializer(project)

    response = build_success_response(serializer.data)
    return JsonResponse(response.serialize(), safe = False)

@api_view(["DELETE"])
def delete_project(request, id):
    id = int(id)

    Project.objects.filter(id = id).delete()

    response = build_success_response({})
    return JsonResponse(response.serialize(), safe = False)

"""
Example request:
{
    "signature": 285791875916831451956391589159,
    "data": {
        "timestamp": 1878958752,
        "note": "Lorem ipsum"
    }
}
"""
@api_view(["POST"])
def approve(request, project_id, employee_id):
    id = int(project_id)
    employee_id = int(employee_id)
    employee = Employee.objects.get(id = employee_id)
    project = Project.objects.get(id = id)

    # construct block
    approval = Approval(
        project = project,
        data = json.dumps(request.data["data"]),
        signature = request.data["signature"],
        employee = employee,
    )
    # check for validity
    success = approval.validate_request()
    if not success:
        response = build_fail_response({
            "message": "Block is not valid!",
        })
        return JsonResponse(response.serialize(), safe = False)

    approval.previous_hash = project.tail_hash
    approval.generate_hash()
    project.tail_hash = approval.hash
    approval.save()

    # set checklist_mask
    if project.head_hash == NO_DATA_HASH:
        project.head_hash = approval.hash
    project.set_checklist_mask(employee.level_id)
    project.save()

    # TODO: publish message if pass the threshold

    serializer = ApprovalSerializer(approval)
    response = build_success_response({
        "approval": serializer.data
    })
    return JsonResponse(response.serialize(), safe = False)