# Evaluate user roles decorator
def roles(*roles):
    def request_wrapper(func):
        rls = []
        rls.append(lambda cls: cls._user.get_user_roles())

        def wrapper(cls, *args, **kwargs):
            r = [x(cls) for x in rls if x(cls)]
            assert roles in cls._user.get_user_roles(), 'User doesnt have roles: %' % r
            returned_value = func(*args, **kwargs)
            return returned_value

        return wrapper

    return request_wrapper
