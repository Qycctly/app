import time

# def metric(func):
#     import time
#     def wrapper(*args, **kw):
#         start = time.time()
#         result = func(*args, **kw)
#         end = time.time()
#         print('%s executed in %s ms' % (func.__name__, end-start))
#         return result
#     return wrapper
db = {
    'michael': 'e10adc3949ba59abbe56e057f20f883e',
    'bob': '878ef96e86145580c38c87f0410ad153',
    'alice': '99b1c2188db85afee403b1536010c2c9'
}

def login(user, password):
    import hashlib
    input_md5 = hashlib.md5()
    input_md5.update(password.encode('utf-8'))
    db_md5 = db[user]
    if input_md5.hexdigest() == db_md5:
        return True
    return False
print(login('michael', '123456'))

print('ok')