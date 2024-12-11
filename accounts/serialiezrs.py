from rest_framework import serializers
from django.db import transaction
from django.db.models import F
from .models import User, Account, Transaction
import logging
from django.db import DatabaseError
from .tasks import *

logger = logging.getLogger(__name__)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserBalanceSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(source='user.phone_number', read_only=True)
    class Meta:
        model = Account
        fields = ["phone_number", "balance"]

class TransactionSerializer2(serializers.ModelSerializer):
    balance = serializers.CharField(source="sender.balance", read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'sender', 'receiver', 'amount', 'status', 'balance']
        # fields = "__all__"
        read_only_fields = ['id', 'created_at', 'status', 'sender', 'balance']

    def validate(self, data):
        user = self.context['request'].user
        print(user)
        sender = user.account
        print("sssssssssssssssssssssssssssssssssssssssssssss")
        print(sender)
        # sender = self.context['request'].user.se
        # sender = data.get('sender')
        receiver = data.get('receiver')
        amount = data.get('amount')

        if sender == receiver:
            raise serializers.ValidationError("Sender and receiver cannot be the same account.")

        if amount <= 0:
            raise serializers.ValidationError("The transfer amount must be greater than zero.")

        if sender.balance < amount:
            raise serializers.ValidationError("Insufficient balance in the sender's account.")

        return data

    def create(self, validated_data):
        sender = self.context['request'].user.account

        # sender = user.t
        receiver = validated_data['receiver']
        amount = validated_data['amount']
        with transaction.atomic():
            sender_account = sender.__class__.objects.select_for_update().get(pk=sender.pk)
            print(sender_account)
            if sender_account.balance < amount:
                raise serializers.ValidationError("Insufficient balance in the sender's account.")


            sender.balance -= amount
            sender.save()

            receiver.balance += amount
            receiver.save()

            # Save the transaction
            transaction_record = Transaction.objects.create(
                sender=sender,
                receiver=receiver,
                amount=amount,
                status='SUCCESS'
            )
            return transaction_record








class TransactionSerializer(serializers.ModelSerializer):
    # balance = serializers.CharField(source="sender.balance", read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'sender', 'receiver', 'amount', 'status']
        read_only_fields = ['id', 'created_at', 'status', 'sender']

    def validate(self, data):
        user = self.context['request'].user
        sender_account = user.account
        receiver_account = data.get('receiver')
        transfer_amount = data.get('amount')

        self.validate_sender_receiver(sender_account, receiver_account)
        self.validate_transfer_amount(transfer_amount)

        return data

    def validate_sender_receiver(self, sender, receiver):
        if sender == receiver:
            raise serializers.ValidationError("Sender and receiver cannot be the same account.")

    def validate_transfer_amount(self, amount):
        if amount <= 0:
            raise serializers.ValidationError("The transfer amount must be greater than zero.")

    def create(self, validated_data):
        sender_account = self.context['request'].user.account
        receiver_account = validated_data['receiver']
        transfer_amount = validated_data['amount']

        while True:
            try:
                with transaction.atomic():
                    # Lock the sender account for update
                    sender_account = sender_account.__class__.objects.select_for_update().get(pk=sender_account.pk)

                    # Check if the sender has sufficient balance
                    if sender_account.balance < transfer_amount:
                        raise serializers.ValidationError("Insufficient balance in the sender's account.")

                    # Update balances using F expressions to avoid race conditions
                    sender_account.balance = F('balance') - transfer_amount
                    receiver_account.balance = F('balance') + transfer_amount
                    sender_account.save()
                    receiver_account.save()

                    # Create the transaction record
                    transaction_record = Transaction.objects.create(
                        sender=sender_account,
                        receiver=receiver_account,
                        amount=transfer_amount,
                        status='SUCCESS'
                    )

                    logger.info(f"Transaction successful: {transaction_record.id} from {sender_account.id} to {receiver_account.id} of amount {transfer_amount}")
                    return transaction_record

            except DatabaseError as e:
                # Handle the case where the transaction fails due to a concurrency issue
                logger.warning(f"Transaction failed due to a database error: {e}. Retrying...")
                continue






class OrderTransactionSerializer(serializers.ModelSerializer):
    balance = serializers.CharField(source="sender.balance", read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'sender', 'receiver', 'amount', 'status', 'balance']
        read_only_fields = ['id', 'created_at', 'status', 'sender', 'balance']

    def validate(self, data):
        user = self.context['request'].user
        sender = user.account
        receiver = data.get('receiver')
        amount = data.get('amount')

        if sender == receiver:
            raise serializers.ValidationError("Sender and receiver cannot be the same account.")

        if amount <= 0:
            raise serializers.ValidationError("The transfer amount must be greater than zero.")

        if sender.balance < amount:
            raise serializers.ValidationError("Insufficient balance in the sender's account.")

        return data

    def create(self, validated_data):
        sender = self.context['request'].user.account
        receiver = validated_data['receiver']
        amount = validated_data['amount']

        # Call the Celery task asynchronously
        result = process_transaction.apply_async(
            (sender.id, receiver.id, amount)
        )

        # Return the transaction result (optional, depending on how you want to handle it)
        return {
            "transaction_id": result.id,
            "status": "Transaction processing in background"
        }
