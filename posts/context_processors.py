from .models import Notification

def unread_notifications_count(request):
    if request.user.is_authenticated:
        count = request.user.notification_set.filter(is_read=False).count()
    else:
        count = 0
    return {'unread_notifications_count': count}