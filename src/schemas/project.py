def projectEntity(item) -> dict:
    return {
        "id":  str(item["_id"]),
        "title":  item["title"],
        "description":  item["description"],
        "due_date":  item["due_date"],
        "admin": item['admin'],
        "members": item['members']
    }

def projectsEntity(entity) -> list:
    return [projectEntity(item) for item in entity]