# from werkzeug.security import generate_password_hash, check_password_hash
# import requests, json


# def md5(string):
# 	md5 = requests.get('https://api.hashify.net/hash/md4/hex?value=' + string)
# 	print(md5)
# 	return md5

# def set_password(password):
#     return generate_password_hash(password)

# def check_password(password_hash, password):
#     return check_password_hash(password_hash, password)

def avatar(size, email):
    digest = email
    return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
    digest, size)