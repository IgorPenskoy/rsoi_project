import gitlab

from .constants import GITLAB_URL
from .models import Repository


def get_gitlab_instance():
    gl = gitlab.Gitlab(GITLAB_URL)
    return gl


def get_gitlab_instance_auth(private_token):
    gl = gitlab.Gitlab(GITLAB_URL, private_token)
    gl.auth()
    return gl


def update_repository_info(repository_id):
    gl = get_gitlab_instance()
    project = gl.projects.get(repository_id)
    Repository.objects.filter(id=repository_id).update(url=project.web_url,
                                                       repository=project.name,
                                                       last_activity=project.last_activity_at)


def create_repository(repository_name, private_token):
    gl = get_gitlab_instance_auth(private_token)
    project = gl.projects.create({'name': repository_name, 'visibility': 'public'})
    Repository.objects.create(id=project.id,
                              url=project.web_url,
                              username=project.owner["username"],
                              repository=project.name,
                              last_activity=project.last_activity_at)
