from django.urls import path
from system.views import employeelevel, employee, smartcontract, project

urlpatterns = [
    path("levels", employeelevel.levels, name = "levels"),
    path("levels/add", employeelevel.add_level, name = "add_level"),
    path("levels/<int:id>", employeelevel.get_level, name = "get_level"),
    path("levels/<int:id>/update", employeelevel.update_employee_level, name = "update_employee_level"),
    path("levels/<int:id>/delete", employeelevel.delete_level, name = "delete_level"),

    # employee
    path("employees", employee.get_all_employees, name = "get_all_employees"),
    path("employees/add", employee.add_employee, name = "add_employee"),
    path("employees/<int:id>", employee.get_employee, name = "get_employee"),
    path("employees/<int:id>/update", employee.update_employee, name = "update_employee"),
    path("employees/<int:id>/update_public_key", employee.update_public_key, name = "update_public_key"),
    path("employees/<int:id>/delete", employee.delete_employee, name = "delete_employee"),

    # smart contract
    path("contracts", smartcontract.get_all_contracts, name = "get_all_contracts"),
    path("contracts/add", smartcontract.add_contract, name = "add_contract"),
    path("contracts/<int:id>", smartcontract.get_contract, name = "get_contract"),
    path("contracts/<int:id>/delete", smartcontract.delete_contract, name = "delete_contract"),

    # project
    path("projects", project.get_all_projects, name = "get_all_projects"),
    path("projects/add", project.add_new_project, name = "add_new_project"),
    path("projects/<int:id>", project.get_project, name = "get_project"),
    path("projects/<int:id>/update", project.update_project, name = "update_project"),
    path("projects/<int:id>/delete", project.delete_project, name = "delete_project"),

    # approve
    path("projects/<int:project_id>/approve/<int:employee_id>", project.approve, name = "approve"),
]