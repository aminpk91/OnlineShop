import random

from django.conf import settings
from kavenegar import *
from django.core.cache import cache

#phone_cache = caches['phone_verification']



def phone_verification(id,phone):

    def verify_code_gen(id):
        if not cache.get(f"code:{id}"):
            code = random.randint(10000, 99999)
            cache.set(f"code:{id}", code, 2 * 60)
        return code
    try:
        code = verify_code_gen(id)
        api = KavenegarAPI(settings.PHONE_API)
        params = {'sender': '', 'receptor': phone, 'message': f'کدتایید شما در فروشگاه تولباکس ایران:{code}'}
        response = api.sms_send(params)
        print(response)
        return response

    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)



