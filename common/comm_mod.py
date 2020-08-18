# 공통 모듈
from django.core.paginator import Paginator

def pass_rand(n):
    import random
    str = "abcdefghijklmnopqrstuvwxyz"
    num = "0123456789"
    new_pass = ""
    for i in range(1, n+1):
        if i % 2 == 0:
            new_pass += random.choice(num)
        else:
            new_pass += random.choice(str)
    return new_pass

def page_navi(obj,page,pagecut):
    import math
    paginator = Paginator(obj,pagecut)
    page_obj = paginator.get_page(page)
    page_obj.e_number = math.ceil(page_obj.paginator.count / page_obj.paginator.per_page)
    return page_obj