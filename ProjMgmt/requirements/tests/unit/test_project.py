from django.test import TestCase
from django.contrib.auth.models import User
from requirements import models
from requirements.models import project
from requirements.models import project_api
from requirements.models import user_association
from requirements.models import user_manager
from requirements.models import story 
from requirements.models.project import Project
from requirements.models.user_association import UserAssociation
from requirements.models.iteration import Iteration
from requirements.models.story import Story
import datetime

class Obj(): pass

class ProjectTestCase(TestCase):
    
    def setUp(self):
        self.__clear()
        
        self.__user = User(username="testUser", password="pass")
        self.__user.save()
        
    def tearDown(self):
        self.__clear()
        
    def __clear(self):
        UserAssociation.objects.all().delete
        Project.objects.all().delete
        User.objects.all().delete
        
    def test_get_all_projects_none(self):
        self.assertEqual( models.project_api.get_all_projects().count(), 0)
        
    def test_get_all_projects_one(self):
        p = Project(title="title", description="desc")
        p.save()
        self.assertEqual( models.project_api.get_all_projects().count(), 1)

    def test_get_all_projects_two(self):
        p = Project(title="title", description="desc")
        p.save()
        
        p2 = Project(title="title2", description="desc2")
        p2.save()
        
        self.assertEqual( models.project_api.get_all_projects().count(), 2)
        
    def test_get_all_projects_for_user_none(self):
        p = Project(title="title", description="desc")
        p.save()
        self.assertEqual( models.project_api.get_projects_for_user(self.__user.id).count(), 0)
        
    def test_get_all_projects_for_user_one(self):
        p = Project(title="title", description="desc")
        p.save()
        
        u = UserAssociation(user = self.__user, project=p)
        u.save()
        
        self.assertEqual( models.project_api.get_projects_for_user(self.__user.id).count(), 1)    
           
    def test_can_user_access_project_cant(self):
        p = Project(title="title", description="desc")
        p.save()
        self.assertEqual( models.project_api.can_user_access_project(self.__user.id, p.id), False)    
        
    def test_can_user_access_project_can(self):
        p = Project(title="title", description="desc")
        p.save()
        u = UserAssociation(user = self.__user, project=p)
        u.save()
        self.assertEqual( models.project_api.can_user_access_project(self.__user.id, p.id), True)        
        
    def test_project_get_iterations_for_project_none(self):
        p = Project(title="title", description="desc")
        p.save()
        iterations = models.project_api.get_iterations_for_project(p)
        self.assertEqual(False, iterations.exists())
        
    def test_project_get_iterations_for_project_one(self):
        p = Project(title="title", description="desc")
        p.save()
        
        models.project_api.add_iteration_to_project("title", 
                                                    "desc", 
                                                    "2015-01-01", 
                                                    "2015-02-01", 
                                                    p.id)
        iterations = models.project_api.get_iterations_for_project(p)
        self.assertEqual(True, iterations.exists())
    
    
    #===========================================================================
    # aidan: this method doesn't exist in production yet
    # def test_createUser(self):
    #     req = Obj()
    #     req.POST = {'username' : 'user', 'password' : 'pass'}
    #     models.user_manager.createUser(req)
    #      
    #     u = User.objects.all()[1]
    #     self.assertEqual('user', u.username)
    #     self.assertEqual(False, u.is_active)
    #===========================================================================
        
    def test_project_get_stories_for_project_none(self):
        p = Project(title="title", description="desc")
        p.save()
        iterations = models.project_api.get_iterations_for_project(p)
        stories = models.story.get_project_stories(p.id)
        self.assertEqual(False, stories.exists())
        
    def test_project_get_stories_for_project_one(self):
        p = Project(title="title", description="desc")
        p.save()
        models.story.create_story(self.__user, p, {"title" : "title",
                                                   "description" : "desc",
                                                   "reason" : "reason",
                                                   "test" : "test",
                                                   "status" : 1})
        
        iterations = models.project_api.get_iterations_for_project(p)
        stories = models.story.get_project_stories(p.id)
        self.assertEqual(True, stories.exists())
        