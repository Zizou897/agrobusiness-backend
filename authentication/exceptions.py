from rest_framework.exceptions import APIException


class VendorNotAuthorizedError(APIException):
    status_code = 401
    default_detail = "Vous n'êtes pas autorisé à vous connecter à la plateforme client, si vous êtes un vendeur veuillez vous connecter à la plateforme vendeur."
    default_code = "vendor_not_authorized"


class ClientNotAuthorizedError(APIException):
    status_code = 401
    default_detail = "Vous n'êtes pas autorisé à vous connecter à la plateforme vendeur, si vous êtes un client veuillez vous connecter à la plateforme client"
    default_code = "client_not_authorized"


class OldPasswordNotCorrectError(APIException):
    status_code = 400
    default_detail = "L'ancien mot de passe n'est pas correct."
    default_code = "old_password_not_correct"


class OldPaswwordAndNewPasswordAreSameError(APIException):
    status_code = 400
    default_detail = "L'ancien mot de passe et le nouveau mot de passe sont les mêmes."
    default_code = "old_password_and_new_password_are_same"


class PasswordsNotMatchError(APIException):
    status_code = 400
    default_detail = "Les mots de passe ne correspondent pas."
    default_code = "passwords_not_match"


class LoginFailedError(APIException):
    status_code = 401
    default_detail = "Le nom d'utilisateur ou le mot de passe est incorrect."
    default_code = "login_failed"


class EmailAlreadyExistsError(APIException):
    status_code = 401
    default_detail = "Un utilisateur avec cette adresse email existe déjà."
    default_code = "email_already_exists"


class UsernameAlreadyExistsError(APIException):
    status_code = 401
    default_detail = "Un utilisateur avec ce nom d'utilisateur existe déjà."
    default_code = "username_already_exists"


class UsernameOrEmailAlreadyExistsError(APIException):
    status_code = 401
    default_detail = (
        "Un utilisateur avec ce nom d'utilisateur ou cette adresse email existe déjà."
    )
    default_code = "username_or_email_already_exists"


class UserNotActiveError(APIException):
    status_code = 401
    default_detail = "Le compte n'est pas encore vérifié , veuillez réessayer le processus de vérification."
    default_code = "user_not_active"


class UserRegistrationNotCompleteError(APIException):
    status_code = 401
    default_detail = (
        "L'inscription n'est pas encore terminée, veuillez recommencer celle-ci ."
    )
    default_code = "user_registration_not_complete"


class NotAccountLinkedToThisProfileError(APIException):
    status_code = 401
    default_detail = "Aucun compte n'est lié à ce profil."
    default_code = "not_account_linked_to_this_profile"


class UserNotFoundError(APIException):
    status_code = 401
    default_detail = "L'utilisateur n'existe pas."
    default_code = "user_not_found"


class CodeNotCorrectError(APIException):
    status_code = 401
    default_detail = "Le code est incorrect."
    default_code = "code_not_correct"
