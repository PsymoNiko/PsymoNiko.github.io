import logging
from locust import HttpUser, task, between, SequentialTaskSet
import random
import json

# Configure loggers
logging.basicConfig(level=logging.INFO)

# Success logger
success_logger = logging.getLogger("success_logger")
success_handler = logging.FileHandler("success.log")
success_formatter = logging.Formatter('%(asctime)s - %(message)s')
success_handler.setFormatter(success_formatter)
success_logger.addHandler(success_handler)

# Error logger
error_logger = logging.getLogger("error_logger")
error_handler = logging.FileHandler("error.log")
error_formatter = logging.Formatter('%(asctime)s - %(message)s')
error_handler.setFormatter(error_formatter)
error_logger.addHandler(error_handler)

# Exception logger
exception_logger = logging.getLogger("exception_logger")
exception_handler = logging.FileHandler("exception.log")
exception_formatter = logging.Formatter('%(asctime)s - %(message)s')
exception_handler.setFormatter(exception_formatter)
exception_logger.addHandler(exception_handler)


class TransactionBehavior(SequentialTaskSet):
    lis = ["09102001647", "09123456789", "09123456788"]

    def on_start(self):
        try:
            # Login to get JWT token before making any requests
            response = self.client.post("/api/token/", json={
                "phone_number": random.choice(self.lis),
                "password": "1234"
            })
            if response.status_code == 200:
                # Extract JWT token from the response
                self.token = response.json()["access"]
                success_logger.info(f"Login successful for user {response.request.body}")
            else:
                self.token = None
                error_logger.error(f"Login failed for user {response.request.body} with status {response.status_code}")
        except Exception as e:
            self.token = None
            exception_logger.exception(f"Login exception: {e}")

    @task
    def create_transaction(self):
        if self.token:
            payload = {
                "receiver": 3,
                "amount": 1
            }
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }
            try:
                # Send POST request to the /user/transaction/ endpoint with JWT token
                response = self.client.post("/user/transaction/", json=payload, headers=headers)
                if response.status_code == 200:
                    success_logger.info(f"Transaction created successfully: {payload}")
                else:
                    error_logger.error(f"Failed to create transaction: {response.status_code} | Payload: {payload}")
            except Exception as e:
                exception_logger.exception(f"Transaction exception: {e} | Payload: {payload}")
        else:
            error_logger.error("Token is missing, can't create transaction.")


class UserBehavior(HttpUser):
    wait_time = between(1, 5)  # Wait time between tasks, 1-5 seconds
    tasks = [TransactionBehavior]
