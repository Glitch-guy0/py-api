# Auth Service

This microservice handles user authentication using FastAPI and Okta OIDC integration. It follows a modular architecture for scalability and maintainability.

## Project Structure

#### api/
- Contains all API endpoint routes
- Handles HTTP requests and responses
- Defines route handlers and middleware
- Key files:
  - `auth.py`: OAuth2/OIDC authentication routes
    - `user_login()`: OAuth2 login endpoint
    - `user_callback()`: OAuth2 callback endpoint

#### lib/
- Contains core business logic and utility classes
- Implements authentication flows and token handling
- Key files:
  - `oidc_client.py`: OIDC authentication implementation
    - OAuth2/OIDC flow management
    - Token and user data handling

#### models/
- Contains database schema definitions
- Defines data structures and relationships
- Key files:
  - `state_token.py`: State token schema

#### repositories/
- Database access layer abstraction
- Implements CRUD operations
- Key files:
  - `state_token.py`: State token database operations
    - Token storage and retrieval
    - Token validation

#### tests/
- Test suite implementation
- Unit and integration tests
- Test utilities and fixtures

#### config/
- Environment configuration management
- Configuration loading and validation
- Environment variable handling

### Root Files

#### main.py
- Application bootstrap
- FastAPI app initialization
- Route registration
- Middleware setup
