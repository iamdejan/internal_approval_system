from django.http import JsonResponse

from rest_framework.decorators import api_view

from system.models import SmartContract, build_fail_response, build_success_response
from system.serializers import SmartContractSerializer

@api_view(["GET"])
def get_all_contracts(request):
    contracts = SmartContract.objects.all()
    serializer = SmartContractSerializer(contracts, many = True)

    response = build_success_response(serializer.data)
    return JsonResponse(response.serialize(), safe = False)

@api_view(["POST"])
def add_contract(request):
    data = request.data
    contract_code = data["contract_code"]
    threshold = int(data["threshold"])
    description = data["description"]

    contract = SmartContract(
        contract_code = contract_code,
        threshold = threshold,
        description = description
    )
    contract.save()
    serializer = SmartContractSerializer(contract)

    response = build_success_response(serializer.data)
    return JsonResponse(response.serialize(), safe = False)

@api_view(["GET"])
def get_contract(request, id):
    id = int(id)
    contract = SmartContract.objects.get(id = id)
    serializer = SmartContractSerializer(contract)

    response = build_success_response(serializer.data)
    return JsonResponse(response.serialize(), safe = False)

@api_view(["DELETE"])
def delete_contract(request, id):
    id = int(id)
    SmartContract.objects.filter(id = id).delete()

    response = build_success_response({})
    return JsonResponse(response.serialize(), safe = False)