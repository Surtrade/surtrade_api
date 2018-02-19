from enum import Enum


class MethodsEnum(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"

class BeaconTypeEnum(Enum):
    DOOR = "Door"
    INNER = "Inner"

class SecurityLevelEnum(Enum):
    NO_CREDENTIALS = 0
    AUTH_ANY_USER = 1
    AUTH_AS_USER = 1
    AUTH_AS_AGENT = 1
    AUTH_AS_CUSTOMER = 1
    AUTH_AS_ADMIN = 2
    CONTRACT = 3