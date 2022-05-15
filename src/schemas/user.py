def userEntity(item) -> dict:
    return {
        "id":  str(item["_id"]),
        "first_name":  item["first_name"],
        "last_name":  item["last_name"],
        "email":  item["email"],
        "password":  item["password"],
        "user_type": item["user_type"]
    }

def usersEntity(entity) -> list:
    return [userEntity(item) for item in entity]
