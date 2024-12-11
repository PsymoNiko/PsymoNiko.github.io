from celery import shared_task


from celery import shared_task
from django.db import transaction
from rest_framework.exceptions import ValidationError
from .models import Transaction, Account

# @shared_task
# def process_order(order_data):
#
#
#     # Step 1: Validate order
#     if not validate_order(order_data):
#         raise ValueError("Invalid order data")
#
#     # Step 2: Process payment
#     if not process_payment(order_data):
#         raise ValueError("Payment failed")
#
#     # Step 3: Ship order
#     if not ship_order(order_data):
#         raise ValueError("Shipping failed")
#
#     return "Order processed successfully"



@shared_task
def process_transaction(sender_id, receiver_id, amount):
    try:
        # Fetch sender and receiver accounts
        sender = Account.objects.get(id=sender_id)
        receiver = Account.objects.get(id=receiver_id)

        # Start a transaction block to ensure atomicity
        with transaction.atomic():
            # Lock the sender account for update to avoid race conditions
            sender_account = sender.__class__.objects.select_for_update().get(pk=sender.pk)

            if sender_account.balance < amount:
                raise ValidationError("Insufficient balance in the sender's account.")

            # Update sender's and receiver's balances
            sender_account.balance -= amount
            sender_account.save()

            receiver.balance += amount
            receiver.save()

            # Create transaction record
            transaction_record = Transaction.objects.create(
                sender=sender_account,
                receiver=receiver,
                amount=amount,
                status='SUCCESS'
            )

            return transaction_record.id

    except Exception as e:
        raise ValidationError(f"Transaction failed: {str(e)}")
