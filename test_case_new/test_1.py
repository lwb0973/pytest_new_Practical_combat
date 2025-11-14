from settings import var


def test_token(sc_login):
    setattr(var, 'token', sc_login)
