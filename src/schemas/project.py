from models.project import ProjectModel


def projectEntity(item: ProjectModel) -> dict:
    return {
        "id":  item.id,
        "title":  item.title,
        "description":  item.description,
        "due_date":  item.due_date,
        "admin": item.admin,
        "members": item.members,
        "invitees": item.invitees
    }


def projectsEntity(entity) -> list:
    return [projectEntity(item) for item in entity]

def projectEntityGet(item: ProjectModel) -> dict:
    return {
        "id":  str(item["_id"]),
        "title":  item.title,
        "description":  item.description,
        "due_date":  item.due_date,
        "admin": item.admin,
        "members": item.members,
        "invitees": item.invitees
    }