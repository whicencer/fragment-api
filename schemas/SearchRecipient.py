from pydantic import BaseModel

class SearchRecipientDto(BaseModel):
  username: str

class SearchRecipientResponse(BaseModel):
  ok: bool
  recipient_id: str
  name: str
  photo: str