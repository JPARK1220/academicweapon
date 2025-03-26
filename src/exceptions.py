from fastapi import HTTPException

# 404
class UnauthorizedHTTPRequest(HTTPException):
  def __init__(self):
    super().__init__(
      status_code=404,
      detail=f"Insufficient credentials provided.",
    )