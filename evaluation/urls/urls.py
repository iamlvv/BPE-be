from evaluation.urls.main import urlpatterns_main
from evaluation.urls.bpmn_file import urlpatterns_bpmn_file
from evaluation.urls.evaluate import urlpatterns_evaluate
from evaluation.urls.project import urlpatterns_project
from evaluation.urls.user import urlpatterns_user


urlpatterns = urlpatterns_main + urlpatterns_bpmn_file + \
    urlpatterns_evaluate + urlpatterns_project + urlpatterns_user
