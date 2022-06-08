from models.task import TaskModel


def taskEntity(item: TaskModel) -> dict:
    return {
        "id":  item.id,
        "title":  item.title,
        "description":  item.description,
        "due_date":  item.due_date,
        "status": item.status,
        "asignee": item.asignee,
        "project": item.project
    }


def tasksEntity(entity) -> list:
    return [taskEntity(item) for item in entity]

def taskEntityGet(item: TaskModel) -> dict:
    return {
        "id":  str(item.id),
        "title":  item.title,
        "description":  item.description,
        "due_date":  item.due_date,
        "status": item.status,
        "asignee": item.asignee,
        "project": item.project
    }