""" View classes for our API """
# Annotations, OR Queries (Q), aggregation with Sum.
from django.db.models import F, Q, Sum
# To create Token for registered user
from rest_framework.authtoken.models import Token
# To add transaction nested url inside wallet
from rest_framework.decorators import action
# JSON Responses
from rest_framework.response import Response
# Viewset class to create views
from rest_framework import viewsets
# To assign authentication method.
from rest_framework.authentication import TokenAuthentication
# To indicate HTTP status for client
from rest_framework import status
# Permissions to check the user
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from api import serializers
from api import models
import requests


# Create your views here.
class HomeAPI(viewsets.ViewSet):
    """ Home API ViewSet """

    def list(self, request):
        """ Return a hello message  """
        return Response({'message': 'Welcome'})


class CreateUser(viewsets.ModelViewSet):
    """ View class to handle user creation """

    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        """
         Create token for user:
        """
        response = super().create(request, *args, **kwargs)
        instance = response.data
        created_user = models.UserProfile.objects.get(id=int(instance.get('id')))
        token = Token.objects.create(user=created_user)
        return Response({"token": token.key}, status=status.HTTP_201_CREATED)


class WalletViewSet(viewsets.ModelViewSet):
    """ Wallet view class for creating wallet based on authenticated user and return it """
    res = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
    res_js = res.json()
    rate = res_js['bpi']['USD']['rate']
    serializer_class = serializers.WalletSerializer
    queryset = models.Wallet.objects.all().annotate(
        amountUSD=F('amount') * rate
    ).order_by('-id')
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    http_method_names = ['post', 'get']
    lookup_field = "address"
    # lookup_value_regex = "[^/]+"

    # def list(self, request, *args, **kwargs):
    #     """ Return 405 NOT ALLOWED for listing all wallets """
    #     return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def perform_create(self, serializer):
        """ Sets the user profile to the logged in user """
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        """ Handle user wallet count increment and response type after creating object. """
        response = super().create(request, *args, **kwargs)
        instance = response.data
        created_wallet = models.Wallet.objects.get(id=instance.get("id"))
        user = models.UserProfile.objects.get(id=created_wallet.owner.id)
        if user.wallet_count + 1 <= 10:
            user.wallet_count = user.wallet_count + 1
            user.save()
            return Response(
                {"address": created_wallet.address, "balance": created_wallet.amount, "count": user.wallet_count},
                status=status.HTTP_201_CREATED)
        else:
            return Response({"Error": "Maximum wallet"})

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated], url_name="transactions",
            url_path="transactions")
    def transactions(self, request, pk=None, *args, **kwargs):
        """ Nested 'transactions' URL for wallet endpoint to get the transactions of specified wallet. """
        wallet = self.get_object()
        result = models.Transaction.objects.all().filter(
            Q(wallet_to=wallet) | Q(wallet_from=wallet)
        )
        serialized_result = serializers.TransactionSerializer(result, many=True)
        if serialized_result.is_valid:
            return Response(serialized_result.data, status=status.HTTP_200_OK)
        else:
            return Response(serialized_result.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionViewSet(viewsets.ModelViewSet):
    """ View class to handle transaction creation and listing """
    serializer_class = serializers.TransactionSerializer
    queryset = models.Transaction.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    http_method_names = ['post', 'get']

    def get_queryset(self):
        """ Update query to get the transactions of the user who requests """
        transactions = models.Transaction.objects.all().filter(
            Q(wallet_from__owner=self.request.user) | Q(wallet_to__owner=self.request.user))
        return transactions


class StatisticsViewSet(viewsets.ViewSet):
    """ Statistics view for only ADMIN user. Protected with IsAdminUser permission """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminUser)
    http_method_names = ['get']

    def list(self, request):
        """ Update list function to get customized response """
        transactions = models.Transaction.objects.all()
        total = transactions.count()
        total_profit = transactions.aggregate(Sum('fee'))
        return Response({
            'total_transactions': total,
            'total_platform_profit': total_profit['fee__sum']
        }, status=status.HTTP_200_OK)
