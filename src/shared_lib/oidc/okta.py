from dataclasses import dataclass
from typing import Optional


@dataclass
class UserClaims:
    iss: Optional[str] = None
    ver: Optional[str] = None
    sub: Optional[str] = None
    aud: Optional[str] = None
    iat: Optional[str] = None
    exp: Optional[str] = None
    jti: Optional[str] = None
    auth_time: Optional[str] = None
    amr: Optional[str] = None
    idp: Optional[str] = None
    nonce: Optional[str] = None
    name: Optional[str] = None
    nickname: Optional[str] = None
    preferred_username: Optional[str] = None
    given_name: Optional[str] = None
    middle_name: Optional[str] = None
    family_name: Optional[str] = None
    email: Optional[str] = None
    email_verified: Optional[str] = None
    profile: Optional[str] = None
    zoneinfo: Optional[str] = None
    locale: Optional[str] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None
    picture: Optional[str] = None
    website: Optional[str] = None
    gender: Optional[str] = None
    birthdate: Optional[str] = None
    updated_at: Optional[str] = None
    at_hash: Optional[str] = None
    c_hash: Optional[str] = None
