def create_file_key(self, user_id: str, file_uuid: str, file_name: str, file_extension: str):
    return f"uploads/users/{user_id}/images/{file_uuid}/{file_name}.{file_extension}"