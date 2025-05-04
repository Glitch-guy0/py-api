

# Project Structure

src/
│
├── api/                    # HTTP API endpoints and routing
│   └── auth.py             # OAuth2/OIDC login and callback endpoints
│
├── lib/                    # Core authentication logic and helpers
│   └── oidc_client.py      # OIDC client for token and user flow handling
│
├── models/                 # Pydantic or DB schema definitions
│   └── state_token.py      # Schema for state tokens
│
├── repositories/           # Data access and storage logic
│   └── state_token.py      # State token persistence and validation
│
├── config/                 # Configuration management
│   └── env_config.py       # Environment variable loading and validation
│
├── tests/                  # Unit and integration tests
│   ├── conftest.py         # Test fixtures
│   └── test_auth.py        # Auth flow tests
│
└── main.py                 # FastAPI app entrypoint and bootstrap

# Environment Variables
## Service Info
| Variable | Description |
|----------|-------------|
| **SERVICE_NAME** | Name of the microservice |

## Logging
| Variable | Description | Example |
|----------|-------------|----------|
| **LOG_FILE_PATH** | File path for service logs | logs/auth_service.log |
| **LOG_MAX_BYTES** | Max log file size (bytes) | 5242880 (5MB) |
| **LOG_BACKUP_COUNT** | Number of log backups | 3 |
| **SHARED_LIB_LOG_FILE_PATH** | Path to shared library log file | "logs/shared_lib.log" |


## Okta OIDC Configuration
| Variable | Description |
|----------|-------------|
| **OKTA_AUTHORIZE_URI** | Authorization endpoint |
| **OKTA_APPLICATION_REDIRECT_URI** | OAuth redirect URI |
| **OKTA_CLIENT_ID** | OAuth client ID |
| **OKTA_CLIENT_SECRET** | OAuth client secret |
| **OKTA_TOKEN_URI** | Token endpoint URI |
| **OKTA_USERINFO_URI** | User info endpoint URI |
| **OKTA_JWKS_URI** | JWKS (JSON Web Key Set) URI |
| **OKTA_SCOPE** | OAuth scopes (e.g., openid profile email) |
| **OKTA_LOGOUT_URI** | Okta logout endpoint URI |

## OIDC Flow Config
| Variable | Description |
|----------|-------------|
| **POST_LOGOUT_REDIRECT_URI** | Redirect after logout |

## MongoDB Configuration
| Variable | Description |
|----------|-------------|
| **MONGO_URI** | MongoDB URI |
| **MONGO_PORT** | MongoDB port |
| **MONGO_DB_NAME** | Database name |

## Docker Setup

### Dependencies
- **mongo:latest** - MongoDB database container image

### Ports
| Host Port | Container Port | Description |
|-----------|---------------|-------------|
| 8000 | 8000 | FastAPI application |

### Volumes
| Host Path | Container Path | Description |
|-----------|---------------|-------------|
| ./.env | /app/.env | Environment configuration |
| ./logs | /app/logs | Log directory |
| ./src/services/shared_lib | /app/shared_lib | Shared libraries |
| ./requirements.txt | /app/requirements.txt | Python dependencies |