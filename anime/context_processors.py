def notification_context(request):
    if request.user.is_authenticated:
        def get_notification_context():
            user = request.user
            notifications = user.notifications.all()
            return {'all': notifications,
                    'number_of_unread_notification': notifications.filter(unread=True).count()}

        context = get_notification_context()
        return {"notifications": context['all'],
                "number_of_unread_notification": context['number_of_unread_notification']}
    else:
        return {}
