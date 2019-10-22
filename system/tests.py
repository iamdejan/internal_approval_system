from django.test import TestCase

from rest_framework.test import APIRequestFactory

from system.models import EmployeeLevel, Employee
from system.views import employeelevel, employee

import json

def create_dummy_level():
    factory = APIRequestFactory()
    request = factory.post("system/levels/add", {
        "level_name": "JUNIOR_PROGRAMMER",
        "description": "Programming program"
    })

    return employeelevel.add_level(request = request)

def create_dummy_employee(level_id):
    factory = APIRequestFactory()
    request = factory.post("system/employees/add", {
        "first_name": "Giovanni",
        "last_name": "Dejan",
        "username": "iamdejan",
        "level_id": int(level_id),
        "password": "1234efgh"
    })
    response = employee.add_employee(request = request)
    return response

# Create your tests here.
class EmployeeLevelTestCase(TestCase):

    def test_create_level(self):
        first_count = EmployeeLevel.objects.count()

        #Create request to server
        response = create_dummy_level()
        response = json.loads(response.content)

        second_count = EmployeeLevel.objects.count()
        self.assertTrue((second_count - first_count) == 1, "Data is not updated!")
        self.assertIsNotNone(EmployeeLevel.objects.filter(id = response["data"]["id"]))

    def test_get_level(self):
        self.test_create_level()
        id = EmployeeLevel.objects.first().id
        factory = APIRequestFactory()
        request = factory.get("systems/employee/%d" % id)
        response = employeelevel.get_level(request, id)
        self.assertTrue(response.status_code == 200)

        response = json.loads(response.content)
        self.assertIsNotNone(response)

    def test_update_level(self):
        self.test_create_level()

        LEVEL_NAME = "SENIOR_PROGRAMMER"
        DESC = "Lorem ipsum"

        id = EmployeeLevel.objects.first().id
        factory = APIRequestFactory()
        request = factory.put("systems/levels/%d/update" % id, {
            "level_name": LEVEL_NAME,
            "description": DESC
        })

        response = employeelevel.update_employee_level(request, id)
        self.assertEquals(response.status_code, 200)

        response = json.loads(response.content)
        self.assertTrue(response["data"]["level_name"], LEVEL_NAME)
        self.assertTrue(response["data"]["description"], DESC)

        employee_level = EmployeeLevel.objects.get(id = id)
        self.assertTrue(employee_level.level_name, LEVEL_NAME)
        self.assertTrue(employee_level.description, DESC)

    def test_delete_level(self):
        self.test_update_level()

        first_count = EmployeeLevel.objects.count()

        id = EmployeeLevel.objects.first().id
        factory = APIRequestFactory()
        request = factory.delete("systems/levels/%d/delete" % id, {})

        response = employeelevel.delete_level(request, id)
        self.assertEquals(response.status_code, 200)

        second_count = EmployeeLevel.objects.count()
        self.assertTrue((second_count - first_count) == -1, "Data is not updated!")

        count = Employee.objects.filter(id = id).count()
        self.assertEquals(count, 0)

class EmployeeTestCase(TestCase):
    def test_create_employee(self):
        create_dummy_level()

        first_count = Employee.objects.count()

        level_id = EmployeeLevel.objects.first().id
        response = create_dummy_employee(level_id)
        self.assertTrue(response.status_code == 200)

        second_count = EmployeeLevel.objects.count()
        self.assertTrue((second_count - first_count) == 1, "Data is not updated!")

    def test_get_employee(self):
        self.test_create_employee()

        id = Employee.objects.first().id
        factory = APIRequestFactory()
        request = factory.get("system/employees/%d" % id)

        response = employee.get_employee(request, id)
        self.assertTrue(response.status_code == 200)

        response = json.loads(response.content)

        self.assertIsNotNone(response)
        self.assertTrue(response["success"])

    def test_update_employee(self):
        self.test_get_employee()

        id = Employee.objects.first().id
        factory = APIRequestFactory()
        request = factory.put("system/employees/%d/update" % id, {
            "first_name": "Super",
            "last_name": "User",
            "username": "superuser",
            "level_id": EmployeeLevel.objects.last().id,
        })

        response = employee.update_employee(request, id)
        self.assertTrue(response.status_code == 200, "Response is not OK")

        response = json.loads(response.content)
        self.assertIsNotNone(response)

        # re-query
        updated_employee = Employee.objects.get(id = id)
        self.assertEquals(updated_employee.first_name, "Super")
        self.assertEquals(updated_employee.last_name, "User")
        self.assertEquals(updated_employee.username, "superuser")
        self.assertEquals(updated_employee.level_id, EmployeeLevel.objects.last().id)

    def test_delete_employee(self):
        self.test_update_employee()

        id = Employee.objects.first().id
        factory = APIRequestFactory()
        request = factory.delete("system/employees/%d/delete" % id)

        response = employee.delete_employee(request, id)
        self.assertEquals(response.status_code, 200, "Response is not 200!")

        count = Employee.objects.filter(id = id).count()
        self.assertEquals(count, 0, "User isn't deleted")
        pass

class ProjectTestCase(TestCase):
    pass

class SmartContractTestCase(TestCase):
    pass