from django.contrib.auth.models import User

class EmailAuthBackend:
    #authentication user login via using an e-mail address
    
    #this function checks if the psw correct
    def authenticate(self,request,username=None,password=None):
        try:
            # finding the user whose username is email. if not exist, it will call exception
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None
        
        
    # this function checks if the user exist 
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None