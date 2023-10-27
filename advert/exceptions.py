from rest_framework.exceptions import APIException


class OrderQuantityCannotBeGreaterThanProductQuantityError(APIException):
    status_code = 400
    default_detail = "La quantité de la commande ne peut pas être supérieure à la quantité du produit"
    default_code = "order_quantity_cannot_be_greater_than_product_quantity"


class OrderQuantityCannotBeZeroError(APIException):
    status_code = 400
    default_detail = "La quantité de la commande ne peut pas être nulle"
    default_code = "order_quantity_cannot_be_zero"


class OrderQuantityCannotBeNegativeError(APIException):
    status_code = 400
    default_detail = "La quantité de la commande ne peut pas être négative"
    default_code = "order_quantity_cannot_be_negative"


class OnlyOneMainImageAllowedError(APIException):
    status_code = 400
    default_detail = "Seul une image principale est autorisée"
    default_code = "only_one_main_image_allowed"


class OnlyOrderOwnerCanCancelError(APIException):
    status_code = 400
    default_detail = "Seul le propriétaire de la commande peut l'annuler"
    default_code = "only_order_owner_can_cancel"


class OnlyOrderOwnerCanConfirmError(APIException):
    status_code = 400
    default_detail = "Seul le propriétaire de la commande peut la confirmer"
    default_code = "only_order_owner_can_confirm"


class OnlyOrdererCanCommentError(APIException):
    status_code = 400
    default_detail = "Seul un utilisateur qui a déjà commandé le produit peut effectuer un commentaire"
    default_code = "only_orderer_can_comment"


class OwnerOfProductCannotMakeOrderError(APIException):
    status_code = 400
    default_detail = "Le propriétaire du produit ne peut pas effectuer une commande"
    default_code = "owner_of_product_cannot_make_order"


class OnlyOwnerOfCartCanDeleteError(APIException):
    status_code = 400
    default_detail = "Seul le propriétaire du panier peut y supprimer un produit"
    default_code = "only_owner_of_cart_can_delete"


class ProductAlreadyInFavoriteError(APIException):
    status_code = 400
    default_detail = "Le produit est déjà dans la liste des favoris"
    default_code = "product_already_in_favorite"


class ProductOwnerCannotCommentError(APIException):
    status_code = 400
    default_detail = "Le propriétaire du produit ne peut pas effectuer un commentaire"
    default_code = "product_owner_cannot_comment"


class UserMustHasDeliveryAddressError(APIException):
    status_code = 400
    default_detail = "L'utilisateur doit avoir au moins une adresse de livraison"
    default_code = "user_must_has_delivery_address"


class StatusNotValidError(APIException):
    status_code = 400
    default_detail = "Le statut de la commande n'est pas valide"
    default_code = "status_not_valid"
