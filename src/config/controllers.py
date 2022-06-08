from controllers.project import PyMongoProjectsController
from controllers.user import PyMongoUsersController
from controllers.notification import PyMongoNotificationsController

projects_controller = PyMongoProjectsController()
users_controller = PyMongoUsersController()
notifications_controller = PyMongoNotificationsController()
