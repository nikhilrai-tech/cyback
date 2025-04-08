from django.contrib.auth.backends import ModelBackend
# from django.contrib.auth.models import User
from django.db.models import Q
from .models import User

# from .models import Customer

class AuthCustom(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):    
        try:
           # Try to fetch the user by searching the username or email field
            user = User.objects.get(Q(username=username)|Q(email=username))
            # print('entered')
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            return None