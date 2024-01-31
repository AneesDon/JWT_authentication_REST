from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied


class IsSeller(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.user.is_seller:

            return True

        else:
            raise PermissionDenied("You can not access this page because you a buyer")


class IsBuyer(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.user.is_buyer:

            return True

        else:
            raise PermissionDenied("You can not access this page because you a Seller")


