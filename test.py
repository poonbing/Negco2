# import uuid
# import calendar
# from datetime import datetime

# print(uuid.uuid4())
# print(datetime.now())
# num_days = calendar.monthrange(datetime.now().year, datetime.now().month)[1]
# print(num_days)


from cryptography.fernet import Fernet

# Generate a random encryption key
encryption_key = Fernet.generate_key()

print("Generated Encryption Key:", encryption_key.decode())
