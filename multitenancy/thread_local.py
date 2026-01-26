# multitenancy/thread_local.py
from threading import local

_thread_locals = local()


def set_current_user(user):
    _thread_locals.user = user


def get_current_user():
    return getattr(_thread_locals, "user", None)
