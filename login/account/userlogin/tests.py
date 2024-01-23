from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class UserAuthenticationTest(TestCase):
    # enter cmd in project folder, then run commando: python manage.py test <app name>
    def setUp(self):
        # config urls, user reverse('<name of url in urls.py>') to call urls
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.changePSW_url = reverse('change_password')
        self.deletUser_url = reverse('delete_user')
        #set user parameter
        self.user_data = {'username':'tester','first_name':'xin','last_name':'sun',
                         'password':'picapica', 'email':'sxi19@tu-clausthal.de',}
        
        self.user_login_data = {'username':'tester','password':'picapica',}
        
        # create a user manually
        User.objects.create_user(**self.user_data)
        
    def test_registration(self):
        # test user register function
        # create a Http request via POST, submit all user data 
        response = self.client.post(self.register_url, data = self.user_data)
        # HttpResponse code shoule == 200
        self.assertEqual(response.status_code, 200)  

        # check if new user is existed
        new_user = User.objects.get(username='tester')
        self.assertIsNotNone(new_user)
        self.client.logout()
    
    def test_login(self):
        # test user login function
        # after successful login, the site will forward to dashboard.html -> setting: follow = True
        response = self.client.post(self.login_url, data=self.user_login_data, follow=True)
        # check if login successfull
        self.assertEqual(response.status_code, 200)  
        # check if user authentication correctly
        user = User.objects.get(username=self.user_data['username'])
        self.assertTrue(user.is_authenticated)
        self.client.logout()
        
    def test_invalid_login(self):
        # logout current test user
        self.client.logout()
        # test user login function with invalid data
        invalid_data = {'username': 'nonexistentuser', 'password': 'wrongpassword'}
        response = self.client.post(self.login_url, data=invalid_data)
        # website should not be forward to dashboard 
        self.assertNotEqual(response.status_code, 302)  

        # check if user login with invalid_data is false
        self.assertFalse(self.client.login(username=invalid_data['username'], password=invalid_data['password']))
    
    def test_delete_user(self):
        self.client.logout()
        response = self.client.post(self.login_url, data=self.user_login_data, follow=True)
        current_user = User.objects.get(username='tester')
        self.assertTrue(current_user.is_authenticated)
        response=self.client.post(self.deletUser_url, data=self.user_login_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='tester').exists())
        
    