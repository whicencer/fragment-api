from pydantic import BaseModel

class SearchRecipientDto(BaseModel):
  username: str

class RecipientModel(BaseModel):
  recipient_id: str
  name: str
  photo: str

class SearchRecipientResponse(BaseModel):
  ok: bool
  recipient: RecipientModel