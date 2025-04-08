# Auth Service

This microservice is responsible for user authentication. It is built using FastAPI and follows a modular structure to ensure scalability and maintainability.

## Project Structure

The project is organized as follows:

- **api**: This folder contains all the API endpoints. If you plan to add WebSocket support in the future, create a new folder called `sockets` within this directory.
- **lib**: This folder contains all the utility classes and helper functions used across the service.
- **interface**: This folder is designated for creating interface files. These interfaces define the contracts for various components and ensure consistent implementation across the service.
- **models**: This folder contains all the database models. These models are used to interact with the database.
- **repositories**: This folder contains all the abstract classes and interfaces for database operations.
- **tests**: This folder contains all the test cases. It follows the same directory structure as the service to ensure easy navigation and organization.

---

- **config**: This folder is responsible for loading all environment variables from the `.env` file.
- **main.py**: This is the main executable file that starts the FastAPI application.





