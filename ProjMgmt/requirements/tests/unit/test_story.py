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
        