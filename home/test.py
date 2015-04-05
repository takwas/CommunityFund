from django.test import TestCase, Client, TestCase
from home.models import *
from home.forms import *
from django.db import IntegrityError, transaction


class UserProfileTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='user1')
        
        
    def test_userprofile_is_automatic(self):
        
        up1 = UserProfile.objects.get(user_id=self.user.id)
        self.assertTrue(isinstance(up1, UserProfile))
        
    def test_editing_userprofile(self):
        
        #up1 = UserProfile.objects.get(user_id=self.user.id)
        form = ProfileForm({'location': 'Toronto',
                            'interests': 'Art',
                            'cc_number': '9954658471254876', })
        
        self.assertTrue(form.is_valid())
        up1 = form.save()
        
        #response = self.client.post('/user/user1/edit', {'location': 'Toronto',
        #                                       'interests': 'Art',
        #                                       'cc_number': '9954658471254876' },
        #                                        HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        #self.assertEqual(response.status_code, 302)
        #
        #self.assertEqual(repr(up1), "user: user1, location: Toronto, interests: Art")
        
        self.assertTrue(up1.location, "Toronto")
        self.assertTrue(up1.interests, "Art")
        self.assertTrue(up1.cc_number, "9954658471254876")
    
    def test_create_community(self):
        
        pass
    
    def test_join_community(self):
        
        pass
    
    def test_comment_community(self):
        
        pass
    
    def test_create_project(self):
        
        pass
    
    def test_edit_project(self):
        
        pass
    
    def test_delete_project(self):
        
        pass
    
    def test_fund_project(self):
        
        pass
    
    def test_fund_project_goal_reached(self):
        
        pass
    
    def test_rate_project(self):
        
        pass
    
    def test_auto_community_friend_list(self):
        
        
        pass
    
    
    def tearDown(self):
        #self.up1.delete()
        #UserProfile.objects.get(user='1').delete()
        pass
        