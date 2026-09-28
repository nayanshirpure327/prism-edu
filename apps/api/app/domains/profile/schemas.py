from pydantic import BaseModel

class ProfileUpdate(BaseModel):
    full_name: str
    bio: str
