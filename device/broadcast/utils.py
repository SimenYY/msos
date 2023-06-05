import uuid


def generate_random_31_number():
    random_uuid = uuid.uuid4()
    random_str = str(random_uuid).replace('-', '').upper()[:31]
    return random_str
