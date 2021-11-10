import random
from flask_app.models import model_family

def generate_family_code():
    is_not_valid = True
    while is_not_valid:
        code = create_family_code()
        is_not_valid = check_family_code(code)
    return code

def create_family_code():
    # generate random code
    code = ''
    options = [1,2,3,4,5,6,7,8,9,0,'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','!','@','#','$','%','^','&','*']
    for idx in range(10):
        ran_idx = random.randint(0, len(options) - 1)
        code += str(options[ran_idx])
    return code

def check_family_code(code):
    return model_family.Family.get_one(code=code)