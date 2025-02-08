# ChatOnPayment

Welcome to **ChatOnPayment**, an innovative platform designed to integrate seamless chat functionalities with secure payment processing. This repository aims to provide a robust solution for businesses and developers seeking to enhance user engagement through real-time communication while facilitating efficient financial transactions.

## Services Overview

The ChatOnPayment platform comprises several key services, each fulfilling a distinct role within the system:

1. **Accounts Service**: Manages user authentication, authorization, and profile management, ensuring secure access and personalized experiences.

2. **Chat Service**: Facilitates real-time messaging between users, supporting various communication features to enhance interaction.

3. **Payment Service**: Handles payment processing, transaction management, and financial record-keeping, ensuring secure and efficient monetary exchanges.

4. **Core Service**: Acts as the backbone of the platform, coordinating interactions between services and maintaining overall system integrity.

5. **Nginx**: Serves as the reverse proxy and load balancer, directing incoming traffic to the appropriate services and ensuring efficient resource utilization.

6. **Jaeger**: Provides distributed tracing capabilities, allowing for performance monitoring and debugging across services.

7. **Prometheus**: Collects and stores metrics from services, enabling real-time monitoring and alerting to maintain system health.

8. **MinIO**: Offers object storage solutions for handling and storing large amounts of unstructured data, such as chat histories and transaction records.

## Running the Platform with Docker Compose

To deploy the ChatOnPayment platform using Docker Compose, please follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/PsymoNiko/ChatOnPayment.git
   cd ChatOnPayment
   ```

2. **Configure Environment Variables**:
   - Duplicate the `.env.sample` file and rename the copy to `.env`.
   - Open the `.env` file and customize the environment variables as needed to suit your deployment environment.

3. **Build and Start Services**:
   - Ensure Docker and Docker Compose are installed on your system.
   - Execute the following command to build and start all services:
     ```bash
     docker-compose up --build
     ```
   - The `--build` flag ensures that all services are built before starting, incorporating any recent changes.

4. **Access the Platform**:
   - Once all services are running, you can access the platform via the configured Nginx server. By default, it listens on port `80`, so you can navigate to `http://localhost` in your web browser.

5. **Monitor Services**:
   - **Jaeger UI**: Access the Jaeger interface for tracing at `http://localhost:16686`.
   - **Prometheus UI**: Access the Prometheus interface for metrics at `http://localhost:9090`.

6. **Shut Down Services**:
   - To stop all running services, execute:
     ```bash
     docker-compose down
     ```

By following these steps, you will have the ChatOnPayment platform up and running, ready to provide integrated chat and payment services. For further customization and development, refer to the individual service directories and their respective documentation within the repository.

We encourage you to explore and contribute to the project, as collaborative efforts drive innovation and excellence. 
