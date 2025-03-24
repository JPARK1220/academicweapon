from enum import Enum

class Environment(str, Enum):
  DEVELOPMENT = "DEVELOPMENT"
  STAGING = "staging"
  PRODUCTION = "production"