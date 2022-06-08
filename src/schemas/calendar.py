from models.calendar import CalendarModel

def calendarEntity(item: CalendarModel) -> dict:
    return {
        "id":  str(item.id),
        "user_id":  item.user_id,
        "available_times":  item.available_times
    }


def calendarsEntity(entity) -> list:
    print(entity)
    return [calendarEntity(item) for item in entity]
