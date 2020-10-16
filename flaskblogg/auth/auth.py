import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen

AUTH0_DOMAIN = 'coffeestack.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'blog'


class AuthError(Exception):
    """AuthError Exception
    A standardized way to communicate auth failure modes
    """

    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Authorization Header
def get_token_auth_header():
    """
    Obtains the Access Token from the Authorization Header
    """

    # get auth from the header

    # session['profile'] = {
    #     'user_id': userinfo['sub'],
    #     'name': userinfo['name'],
    #     'picture': userinfo['picture']
    # }
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    # split keyword and token
    parts = auth.split()

    # Verify bearer is there
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must begin with "Bearer".'
        }, 401)

    # auth header MUST be two parts
    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    # auth header must have 2 parts
    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    # get token from parts and return
    token = parts[1]
    return token


def check_permissions(permission, payload):
    """
    Ensures that permission exists in payload
    """

    # Ensures that there is permissions field in the payload
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)

    # Ensures that the specific permission exists
    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 401)

    # if conditions pass return true
    return True


def verify_decode_jwt(token):
    '''
    Verifies and decodes the jwt from the given token
    '''

    # process key and header data
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)

    rsa_key = {}

    # Ensure that token header has the kid field
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            # decode token with constant
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        # raise errors where needed
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, ' +
                'check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
        'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
    }, 400)


#use when POST from postman with curl
#this method requires front end to send Beaerer token to the endpoint
#Reference: https://gomakethings.com/using-oauth-with-fetch-in-vanilla-js/
def requires_auth(permission=''):
    '''
    authhentication decorator function
    '''
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator


#use when user logged in, and we store his/her permission in session
#this method requires no front end Bearer token because we use session instead
#Reference: https://community.auth0.com/t/storing-a-users-permissions-when-they-login/36398
def require_auth_from_session():
    '''
    check session
    '''
    from flask import session, Response
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Check to see if it's in their session
            if session is None or 'profile' not in session:
                # If it isn't return our access denied message (you can also return a redirect or render_template)
                return Response("Access denied, please login first")

            # Otherwise just send them where they wanted to go
            return func(*args, **kwargs)

        return wrapper
    return requires_auth_decorator
