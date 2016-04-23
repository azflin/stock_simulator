from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

from stock_simulator_api.models import Portfolio


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user


class IsPortfolioOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of a portfolio to post transactions to it.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            portfolio = Portfolio.objects.get(pk=int(view.kwargs['portfolio_id']))
            user = portfolio.owner
            if user == request.user:
                return True