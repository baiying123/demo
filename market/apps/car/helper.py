from django_redis import get_redis_connection


# 封装json消息
def json_msg(code, msg=None, data=None):
    # code 0为正确
    # 其他为错误
    return {"code": code, "errmsg": msg, "data": data}


def get_car_count(request):
    """获取 当前用户购物车中的总数量 """
    user_id = request.session.get("ID")
    if user_id is None:
        return 0
    else:
        # redis
        r = get_redis_connection()
        # 准备键
        car_key = f"car_{user_id}"
        # 获取
        values = r.hvals(car_key)
        # 准备一个总数量
        total_count = 0
        for v in values:
            total_count += int(v)
        return total_count


# 生成购物车key
def get_car_key(user_id):
    return f"car_{user_id}"
