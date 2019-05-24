# coding: utf-8


class IllegalArgumentException(Exception):

    def __init__(self, *args, **kwargs):
        super(IllegalArgumentException, self).__init__(*args, **kwargs)


class RetryException(Exception):
    def __init__(self, *args, **kwargs):
        super(RetryException, self).__init__(*args, **kwargs)


class NotFoundException(Exception):
    def __init__(self, *args, **kwargs):
        super(NotFoundException, self).__init__(*args, **kwargs)


class CookieExpiredException(Exception):
    def __init__(self, *args, **kwargs):
        super(CookieExpiredException, self).__init__(*args, **kwargs)


class ExitException(Exception):
    def __init__(self, *args, **kwargs):
        super(ExitException, self).__init__(*args, **kwargs)


class CookieNotFoundException(Exception):
    def __init__(self, *args, **kwargs):
        super(CookieNotFoundException, self).__init__(*args, **kwargs)


class CookieNeedUpdateException(Exception):
    def __init__(self, *args, **kwargs):
        super(CookieNeedUpdateException, self).__init__(*args, **kwargs)


class StatusCodeException(Exception):
    def __init__(self, *args, **kwargs):
        super(StatusCodeException, self).__init__(*args, **kwargs)


class InterruptException(Exception):
    def __init__(self, *args, **kwargs):
        super(InterruptException, self).__init__(*args, **kwargs)


class ProxyException(Exception):
    def __init__(self, *args, **kwargs):
        super(ProxyException, self).__init__(*args, **kwargs)
