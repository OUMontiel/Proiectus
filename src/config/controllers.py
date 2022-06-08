from controllers.project import PyMongoProjectsController
from controllers.task import PyMongoTasksController
from controllers.user import PyMongoUsersController

projects_controller = PyMongoProjectsController()
users_controller = PyMongoUsersController()
tasks_controller = PyMongoTasksController()
