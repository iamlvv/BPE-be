from evaluation.views.utils import *


class BPMNFileView:
    @staticmethod
    @api_view(["POST"])
    def save(request):
        file = request.FILES['file']
        project_id = request.POST['project_id']

        fs = FileSystemStorage()

        filename = fs.save('static/' + file.name, file)
        uploaded_file_url = fs.url(filename)

        BPMNFile.insert(uploaded_file_url, project_id)
        return Response("Save successfully")

    @staticmethod
    @api_view(["GET"])
    def get_by_project(request, project_id):
        return BPMNFile.get_by_project(project_id)

    @staticmethod
    @api_view(["GET"])
    def get_by_version(request, version):
        return BPMNFile.get_by_version(version)
