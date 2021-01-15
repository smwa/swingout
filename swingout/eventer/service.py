from typing import List as ListType, Optional

from .models import Event

def get(since: int = -1, maxCount: Optional[int] = None) -> ListType[Event]:
    try:
        events = Event.objects.filter(id__gt=since)
        if maxCount is not None:
            events = events.filter(id__lte=since+maxCount)
        return events.order_by('id')
    except Exception as e:
        print(e)
        return []

def create(name: str, data: dict) -> None:
    event = Event()
    event.name = name
    event.data = data
    event.save()
