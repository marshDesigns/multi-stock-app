from dashboard.cart import Cart
from notifications_app.models import BroadcastNotification
def notifications(request):
    allnotifications = BroadcastNotification.objects.all()
    return {'notifications': allnotifications}

def cart(request):
    return {'cart': Cart(request)}
