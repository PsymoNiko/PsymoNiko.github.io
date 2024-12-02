# chat/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def index(request):
    return render(request, "chat/index.html")


@login_required
def room(request, room_name):
    phone_number = request.user.phone_number  # Assuming you are using Django's built-in authentication
    avatar = request.user.avatar.file.url
    print("skldfjslkfjsdlkjklsdjflksdjflsdfjl")
    print(avatar)
    return render(request, "chat/room.html", {"room_name": room_name, "phone_number": phone_number})
