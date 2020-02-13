from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5

def set_password(password):
    return generate_password_hash(password)

def check_password(password_hash, password):
    return check_password_hash(password_hash, password)

def avatar(size, email):
    digest = md5(email.lower().encode('utf-8')).hexdigest()
    return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
    digest, size)