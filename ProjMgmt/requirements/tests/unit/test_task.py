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
from requirements.models.task import Task
import datetime
from cgi import FieldStorage

class TaskTestCase(TestCase):

    def setUp(self):
        self.__clear()
        self.__project = Project(title="title", description="desc")
        self.__project.save()
        self.__user = User(username="testUser", password="pass")
        self.__user.save()
        
    def tearDown(self):
        self.__clear()
        
    def __clear(self):
        UserAssociation.objects.all().delete
        Project.objects.all().delete
        User.objects.all().delete
        
    def test_get_tasks_for_story(self):
        p = Project(title="title", description="desc")
        p.save()
        s = models.story.create_story(self.__user, self.__project, fields)
        s.save()
        iterations = models.project_api.get_iterations_for_project(p)
        stories = models.story.get_stories_for_project(p.id)
        task = models.task.get_task(s.id)
        self.assertEqual(False, task.exists())
        
    def test_get_tasks_for_story_one(self):
        p = Project(title="title", description="desc")
        p.save()
        models.task.create_task(self.__user, p, {"description" : "description"})
        s = models.story.create_story(self.__user, self.__project, fields)
        iterations = models.project_api.get_iterations_for_project(p)
        stories = models.story.get_project_stories(p.id)
        self.assertEqual(True, task.exists())
    
    def test_create_task_pass(self):
        fields = {"description" : "description"}
        t = model.task.create_task(self.__user, self.__project, self.__story, fields)
        self.assertEqual(1, self.__project.story.task_set.count())
        
    def test_create_task_fail(self):
        fields = {"description" : "description"}
        t = model.task.create_task(self.__user, self.__project, None, fields)
        self.assertEqual(0, self.__project.story.task_set.count())
        
        p = Project(title="title", description="description")
        s = models.story.create_story(self.__user, p, fields)
        t = model.task.create_task(self.__user, p, s, fields)
        self.assertEqual(0, self.__project.story.task_set.count())
        
        
        
        
        
        
        
        
        
        
        
