from rest_framework.exceptions import APIException

class NotAuthorized(APIException):
    status_code = 401
    default_detail = "Vous n'êtes pas autorisé à effectuer cette action"
    default_code = 'not_authorized'