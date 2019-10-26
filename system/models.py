from django.db import models
from django.contrib.auth.models import AbstractUser

from Crypto.PublicKey import RSA
from Crypto.Hash import SHA512

class BaseResponse():
    success = False
    data = {}
    def __str__(self):
        return self.data
    def serialize(self):
        return {
            "success": self.success,
            "data": self.data
        }

def build_success_response(data):
    response = BaseResponse()
    response.success = True
    response.data = data
    return response

def build_fail_response(data):
    response = BaseResponse()
    response.success = False
    response.data = data
    return response

# Create your models here.
class Employee(AbstractUser):
    public_key = models.TextField(null = True, blank=True)
    level = models.ForeignKey("EmployeeLevel", on_delete=models.CASCADE)
    def __str__(self):
        return self.username

class EmployeeLevel(models.Model):
    level_name = models.CharField(max_length = 250)
    description = models.CharField(max_length = 250)
    def __str__(self):
        return self.level_name

class Approval(models.Model):
    hash = models.CharField(max_length = 256, primary_key = True)
    project = models.ForeignKey("Project", on_delete=models.CASCADE)
    data = models.CharField(max_length = 8000, null = False)
    signature = models.CharField(max_length = 1000, null = False)
    previous_hash = models.CharField(max_length = 1000, null = False)
    employee = models.ForeignKey("Employee", on_delete=models.CASCADE)
    def __str__(self):
        return self.employee.username

    def generate_hash(self):
        self.hash = SHA512.new(self.generate_whole_data().encode()).hexdigest()

    def validate_request(self): # return bool
        # import key
        public_key = RSA.importKey(self.employee.public_key)

        # hash sent data
        data_hash = SHA512.new(self.data.encode()).digest()

        # validate
        return public_key.verify(data_hash, (self.signature,))

    """
    Used when we want to publish smart contract
    """
    def generate_whole_data(self):
        whole_data = "%s%s%s%s%s" % (self.project, self.data, self.signature, self.previous_hash, self.employee)
        return whole_data

    def validate_block(self): # return bool
        encrypted_whole_data = SHA512.new(self.generate_whole_data().encode()).digest()
        return self.hash == encrypted_whole_data

class Project(models.Model):
    title = models.CharField(max_length = 250, null = False)
    checklist_mask = models.IntegerField(null = False)
    head_hash = models.CharField(max_length = 256)
    tail_hash = models.CharField(max_length = 256)
    def __str__(self):
        return self.title

    def set_checklist_mask(self, level_id):
        self.checklist_mask |= (1 << (level_id - 1))
        pass

class SmartContract(models.Model):
    contract_code = models.CharField(max_length = 250, null = False, primary_key = True)
    threshold = models.IntegerField(null = False)
    description = models.CharField(max_length = 250)
    def __str__(self):
        return self.contract_code