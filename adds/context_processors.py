from .models import Message


def unread_message_count(request):
    if not request.user.is_authenticated:
        return {"unread_message_count": 0}
    return {"unread_message_count": Message.objects.filter(recipient=request.user, is_read=False).count()}
