from django.http import JsonResponse

from rest_framework.decorators import api_view

from system.models import Approval, build_fail_response, build_success_response
from system.serializers import ApprovalSerializer

@api_view(["GET"])
def get_approval(request, hash):
    approval = Approval.objects.get(hash = hash)
    serializer = ApprovalSerializer(approval)

    response = build_success_response(serializer.data)
    return JsonResponse(response.serialize())

@api_view(["GET"])
def validate(request, hash):
    approval = Approval.objects.get(hash = hash)
    valid = approval.validate_block() and approval.validate_request()
    response = None
    if valid:
        response = build_success_response({})
    else:
        response = build_fail_response({
            "message": "Block is broken"
        })
    return JsonResponse(response.serialize())
