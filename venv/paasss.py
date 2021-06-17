import hashlib, uuid
salt = uuid.uuid4().hex
password="13!#Rafael"
hashed_password = hashlib.sha512(password + salt).hexdigest()
file=open("pass", "w").write(hashed_password)
#tutaj trzeba zahashowac haslo #