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


# Environment Variables

The service requires the following environment variables to be set:

### Service Config
- SERVICE_NAME: Name of the service (default: "auth_service")

### Logging Config
- LOG_FILE_PATH: Path to log file (default: "logs/auth_service.log") 
- LOG_MAX_BYTES: Maximum log file size in bytes (default: 5MB)
- LOG_BACKUP_COUNT: Number of backup log files to keep (default: 3)

### Okta Config
- OKTA_AUTHORIZE_URI: Okta authorization endpoint URL
- OKTA_APPLICATION_REDIRECT_URI: Redirect URI for OAuth flow
- OKTA_CLIENT_ID: OAuth client ID
- OKTA_CLIENT_SECRET: OAuth client secret
- OKTA_TOKEN_URI: Token endpoint URL
- OKTA_USERINFO_URI: User info endpoint URL
- OKTA_JWKS_URI: JSON Web Key Set endpoint URL
- OKTA_SCOPE: OAuth scopes to request
- OKTA_LOGOUT_URI: Logout endpoint URL

### OIDC Config
- POST_LOGOUT_REDIRECT_URI: URI to redirect to after logout

### MongoDB Config
- MONGO_URI: MongoDB connection URI
- MONGO_PORT: MongoDB port number
- MONGO_DB_NAME: MongoDB database name