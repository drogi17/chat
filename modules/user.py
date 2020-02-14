# from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5

# def set_password(password):
#     return generate_password_hash(password)

# def check_password(password_hash, password):
#     return check_password_hash(password_hash, password)

def avatar(email):
    digest = md5(email.lower().encode('utf-8')).hexdigest()
    return 'https://www.gravatar.com/avatar/{}?d=identicon&s=300'.format(
    digest)