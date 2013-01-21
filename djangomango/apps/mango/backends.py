from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login

from registration import signals
from registration.backends.simple import SimpleBackend


class RegistrationBackend(SimpleBackend):
    """ A registration app backend that ignored username. """

    def register(self, request, **kwargs):
        """ Override register since we no longer use username. """

        email, password = kwargs['email'], kwargs['password1']
        user = User.objects.create_user(email, email, password)
        user.first_name = kwargs['first_name']
        user.last_name = kwargs['last_name']
        user.save()           # save name
        user.profile.save()   # save profile to slugify the name

        # authenticate() always has to be called before login(), and
        # will return the user we just created.
        new_user = authenticate(username=email, password=password)
        login(request, new_user)
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        return new_user


class EmailAuthBackend(object):
    """
    Email Authentication Backend
    
    Allows a user to sign in using an email/password pair rather than
    a username/password pair.
    """

    def authenticate(self, username=None, password=None):
        """ Authenticate a user based on email address as the user name. """
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None 

    def get_user(self, user_id):
        """ Get a User object from the user_id. """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
