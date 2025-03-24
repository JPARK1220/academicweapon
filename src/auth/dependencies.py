from .service import AuthService

class AuthDependencies:

  @staticmethod
  def get_auth_service():
    return AuthService