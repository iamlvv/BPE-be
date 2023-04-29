from .main import urlpatterns_main
from .bpmn_file import urlpatterns_bpmn_file
from .evaluate import urlpatterns_evaluate
from .project import urlpatterns_project
from .user import urlpatterns_user
from .result import urlpatterns_result


urlpatterns = urlpatterns_main + urlpatterns_bpmn_file + \
    urlpatterns_evaluate + urlpatterns_project + \
    urlpatterns_user + urlpatterns_result
