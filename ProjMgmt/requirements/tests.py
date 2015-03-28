from django.test import TestCase
import models.project
from models.project import Project
import models.project_api
from models.user_association import UserAssociation
from django.contrib.auth.models import User
import models.user_manager
from models.iteration import Iteration
import datetime
import models.story

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
        
    def test_getAllProjects_none(self):
        self.assertEqual( models.project_api.get_all_projects().count(), 0)
        
    def test_getAllProjects_one(self):
        p = Project(title="title", description="desc")
        p.save()
        self.assertEqual( models.project_api.get_all_projects().count(), 1)

    def test_getAllProjects_one(self):
        p = Project(title="title", description="desc")
        p.save()
        
        p2 = Project(title="title2", description="desc2")
        p2.save()
        
        self.assertEqual( models.project_api.get_all_projects().count(), 2)
        
    def test_getAllProjectsForUser_none(self):
        p = Project(title="title", description="desc")
        p.save()
        self.assertEqual( models.project_api.get_projects_for_user(self.__user.id).count(), 0)
        
    def test_getAllProjectsForUser_one(self):
        p = Project(title="title", description="desc")
        p.save()
        
        u = UserAssociation(user = self.__user, project=p)
        u.save()
        
        self.assertEqual( models.project_api.get_projects_for_user(self.__user.id).count(), 1)    
    
    def test_canUserAccessProject_cant(self):
        p = Project(title="title", description="desc")
        p.save()
        self.assertEqual( models.project_api.can_user_access_project(self.__user.id, p.id), False)    
        
    def test_canUserAccessProject_can(self):
        p = Project(title="title", description="desc")
        p.save()
        u = UserAssociation(user = self.__user, project=p)
        u.save()
        self.assertEqual( models.project_api.can_user_access_project(self.__user.id, p.id), True)        
    
    def test_createUser(self):
        req = Obj()
        req.POST = {'username' : 'user', 'password' : 'pass'}
        models.user_manager.createUser(req)
        
        u = User.objects.all()[1]
        self.assertEqual('user', u.username)
        self.assertEqual(False, u.is_active)
        
    def test_project_no_iterations(self):
        p = Project(title="title", description="desc")
        p.save()
        iterations = models.project_api.get_iterations_for_project(p)
        self.assertEqual(False, iterations.exists())
        
    def test_add_iteration_to_project(self):
        p = Project(title="title", description="desc")
        p.save()
        title = "title"
        description = "description"
        start_date = datetime.date.today()
        end_date = datetime.date.max
        iteration = models.project_api.add_iteration_to_project(title, description, start_date, end_date, p.id)
        
        self.assertEqual(start_date, iteration.start_date)
        self.assertEqual(end_date, iteration.end_date)
        self.assertEqual(title, iteration.title)
        self.assertEqual(description, iteration.description)        
        
        
    def test_add_story_to_iteration(self):
        p = Project(title="title", description="desc")
        p.save()
        title = "title"
        description = "description"
        start_date = datetime.date.today()
        end_date = datetime.date.max
        iteration = models.project_api.add_iteration_to_project(title, description, start_date, end_date, p.id)
        
        story = models.story.create_story({},p,{'title' : "title", 'description' : "description", 'test' : ""})
        
        models.project_api.add_story_to_iteration(story, iteration)
        
        self.assertEqual(iteration,story.iteration)
        
        
    def test_add_story_to_iteration_story_not_in_project(self):
        p = Project(title="title", description="desc")
        p.save()
        title = "title"
        description = "description"
        start_date = datetime.date.today()
        end_date = datetime.date.max
        iteration = models.project_api.add_iteration_to_project(title, description, start_date, end_date, p.id)
        
        p2 = Project(title="title2", description="desc2")
        p2.save()
        
        story = models.story.create_story({},p2,{'title' : "title", 'description' : "description", 'test' : ''})
        try:
            models.project_api.add_story_to_iteration(story, iteration)
            self.fail("Adding a story to an invalid iteration did not throw an exception")
        except(ValueError):
            pass
        
 
    def test_get_iterations_for_project(self):
        p = Project(title="title", description="desc")
        p.save()
        
        iterations = models.project_api.get_iterations_for_project(p)
        self.assertEqual(iterations.count(),0)
        
        title = "title"
        description = "description"
        start_date = datetime.date.today()
        end_date = datetime.date.max
        models.project_api.add_iteration_to_project(title, description, start_date, end_date, p.id)
        
        iterations = models.project_api.get_iterations_for_project(p)
        self.assertEqual(iterations.count(),1)
        
    def test_user_owns_project_true(self):
        owner = User(username="user", password="password", email="email@address.com")
        owner.save()
        
        project = models.project_api.create_project(owner, {'title':'title','description':'description'})
        self.assertEquals(models.project_api.user_owns_project(owner,project), True)
    
    def test_user_owns_project_false(self):
        owner = User(username="user", password="password", email="email@address.com")
        owner.save()
        
        user = User(username="user2", password="password", email="email@address.com")
        user.save()
        
        project = models.project_api.create_project(owner, {'title':'title','description':'description'})
        self.assertEquals(models.project_api.user_owns_project(user,project) , False)   
        
    def test_get_project_stories_for_iteration(self):
        p = Project(title="title", description="desc")
        p.save()
        iteration = models.project_api.add_iteration_to_project("title", "description", datetime.date.today(), datetime.date.max, p.id)
        story = models.story.create_story({},p,{'title' : "title", 'description' : "description", 'test' : ""})
        models.project_api.add_story_to_iteration(story, iteration)  
        stories = models.project_api.get_stories_for_iteration(iteration)

        self.assertEquals(stories.count(), 1)
        self.assertEquals(stories[0], story)
        
        
    def test_get_project_stories_with_no_iteration(self):
        p = Project(title="title", description="desc")
        p.save()
        iteration = models.project_api.add_iteration_to_project("title", "description", datetime.date.today(), datetime.date.max, p.id)
        story = models.story.create_story({},p,{'title' : "title", 'description' : "description", 'test' : ""}) 
        stories = models.project_api.get_stories_with_no_iteration(p)

        self.assertEquals(stories.count(), 1)
        self.assertEquals(stories[0], story)        
       
    def test_get_project_stories_with_no_iteration_none(self):
        p = Project(title="title", description="desc")
        p.save()
        iteration = models.project_api.add_iteration_to_project("title", "description", datetime.date.today(), datetime.date.max, p.id)
        story = models.story.create_story({},p,{'title' : "title", 'description' : "description", 'test' : ""})
        models.project_api.add_story_to_iteration(story, iteration)  
        stories = models.project_api.get_stories_with_no_iteration(iteration)

        self.assertEquals(stories.count(), 0)     