from rest_framework import serializers
from api import models


class UserProfileSerializer(serializers.ModelSerializer):
    """ Serializes a user profile object  """

    class Meta:
        """ Meta information for our serializer  """
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'surname', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password'
                }
            }
        }

    def create(self, validated_data):
        """ Create and return a new user  """
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            surname=validated_data['surname'],
            password=validated_data['password']
        )

        return user


class WalletSerializer(serializers.ModelSerializer):
    """ Serializer class for Wallet Model """
    amountUSD = serializers.DecimalField(max_digits=11, decimal_places=6, read_only=True)

    class Meta:
        """  Meta information for Wallet Serializer """
        model = models.Wallet
        fields = ('id', 'amount', 'address', 'amountUSD')
        extra_kwargs = {
            'amount': {
                'read_only': True,
            }
        }

    def create(self, validated_data):
        """ Update Create function to check can user create or not """
        user = validated_data.get('owner')
        print(user.wallet_count)
        if user.wallet_count < 10:
            wallet = models.Wallet.objects.create(
                owner=user
            )
            return wallet
        else:
            raise serializers.ValidationError("User can't create wallet anymore")


class TransactionSerializer(serializers.ModelSerializer):
    """ Serialize Transaction Model  """
    wallet_from = serializers.CharField(max_length=255)
    wallet_to = serializers.CharField(max_length=255)


    class Meta:
        """ Additional information for serializer """
        model = models.Transaction
        fields = ('id', 'wallet_from', 'wallet_to', 'amount', 'created_at', 'fee')
        extra_kwargs = {
            'fee': {
                'read_only': True
            }
        }

    def create(self, validated_data):
        """ Handle creation to assign wallets and amounts """
        wallet_from = models.Wallet.objects.get(address=validated_data.get('wallet_from'))
        wallet_to = models.Wallet.objects.get(address=validated_data.get('wallet_to'))
        amount = validated_data.get('amount')
        if float(wallet_from.amount) >= float(amount):
            transaction = models.Transaction.objects.create(
                wallet_from=wallet_from,
                wallet_to=wallet_to,
                amount=amount
            )
            wallet_from.amount = wallet_from.amount - amount
            wallet_to.amount = wallet_to.amount + amount
            wallet_to.save()
            wallet_from.save()
        else:
            transaction = {}

        return transaction
