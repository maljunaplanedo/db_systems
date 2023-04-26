import json
import redis
from datetime import datetime


TYPE_BY_NAME = {
    'int': int,
    'str': str,
    'float': float,
    'bool': bool,
    'null': type(None),
    'list': list,
    'dict': dict
}


NAME_BY_TYPE = {
    int: 'int',
    str: 'str',
    float: 'float',
    bool: 'bool',
    type(None): 'null',
    list: 'list',
    dict: 'dict'
}


def measure_time(name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            begin = datetime.now()
            result = func(*args, **kwargs)
            end = datetime.now()

            print(f"Execution time, {name}: {(end - begin).total_seconds():.2f}s")
            return result

        return wrapper
    return decorator


@measure_time("save as string")
def string_save():
    redis.set("string", json_string)


@measure_time("read string")
def string_load():
    return redis.get("string").decode("utf-8")


def string_remove():
    redis.delete("string")


def save_impl(key, obj, writer):
    if isinstance(obj, list) and obj:
        for index, child in enumerate(obj):
            save_impl(key + ":#" + str(index), child, writer)
    elif isinstance(obj, dict) and obj:
        for subkey, child in obj.items():
            save_impl(key + ":@" + subkey, child, writer)
    else:
        writer(key, NAME_BY_TYPE[type(obj)] + '@' + str(obj))


@measure_time("save as hset")
def hset_save():
    save_impl("k", json_value, lambda key, value: redis.hset("hset", key, value))


@measure_time("save as zset")
def zset_save():
    zset_save.idx += 1
    save_impl("k", json_value, lambda key, value: redis.zadd("zset", {key + "\t" + value: zset_save.idx}))


@measure_time("save as list")
def list_save():
    save_impl("k", json_value, lambda key, value: redis.lpush("list", key + "\t" + value))


zset_save.idx = 0


def load_impl(iterable):
    def set_to_list_or_dict(parent, key, child):
        if key.startswith('#'):
            index = int(key[1:])
            if len(parent) <= index:
                parent += [None] * (index - len(parent) + 1)
            parent[index] = child
        else:
            parent[key[1:]] = child

    def restore_typed_object(type_obj_str):
        type_, obj = type_obj_str.split('@', maxsplit=1)
        if type_ == 'null':
            return None
        elif type_ == 'bool':
            return True if obj == 'True' else False
        elif type_ == 'list':
            return []
        elif type_ == 'dict':
            return {}
        else:
            return TYPE_BY_NAME[type_](obj)

    result = None

    for key, value in iterable:
        path = key.split(':')[1:]

        if not path:
            return restore_typed_object(value)

        if result is None:
            if path[0].startswith('#'):
                result = []
            else:
                result = {}

        parent = result
        key_in_parent = path[0]

        for subkey in path[1:]:
            if key_in_parent.startswith('#'):
                index = int(key_in_parent[1:])
                if index < len(parent):
                    current = parent[index]
                else:
                    current = None
            else:
                current = parent.get(key_in_parent[1:])

            if current is None:
                if subkey.startswith('#'):
                    current = []
                else:
                    current = {}
                set_to_list_or_dict(parent, key_in_parent, current)

            parent = current
            key_in_parent = subkey

        obj = restore_typed_object(value)
        set_to_list_or_dict(parent, key_in_parent, obj)

    return result


@measure_time("read hset")
def hset_load():
    def generator():
        items = redis.hgetall("hset").items()
        for key, value in items:
            yield key.decode('utf-8'), value.decode('utf-8')
    return load_impl(generator())


@measure_time("read zset")
def zset_load():
    def generator():
        items = redis.zrange("zset", 0, redis.zcard("zset"))
        for key_value in items:
            yield key_value.decode('utf-8').split('\t', maxsplit=1)
    return load_impl(generator())


@measure_time("read list")
def list_load():
    def generator():
        items = redis.lrange("list", 0, redis.llen("list"))
        for key_value in items:
            yield key_value.decode('utf-8').split('\t', maxsplit=1)
    return load_impl(generator())


def hset_remove():
    redis.delete("hset")


def zset_remove():
    redis.delete("zset")


def list_remove():
    redis.delete("list")


if __name__ == '__main__':
    pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
    redis = redis.Redis(connection_pool=pool)

    with open('input.json') as json_file:
        json_string = json_file.read()

    json_value = json.loads(json_string)

    string_save()
    assert string_load() == json_string
    string_remove()

    hset_save()
    assert hset_load() == json_value
    hset_remove()

    zset_save()
    assert zset_load() == json_value
    zset_remove()

    list_save()
    assert list_load() == json_value
    list_remove()
