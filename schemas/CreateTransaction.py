from pydantic import BaseModel, Field
from typing import List

class WalletAccount(BaseModel):
  address: str
  chain: str
  publicKey: str
  walletStateInit: str

class CreateTransactionDto(BaseModel):
  recipient_id: str
  quantity: int = Field(ge=50, le=1000000)
  account: WalletAccount

class TransactionMessage(BaseModel):
  address: str
  amount: str
  payload: str

class Transaction(BaseModel):
  validUntil: int
  messages: List[TransactionMessage]

class CreateTransactionResponse(BaseModel):
  ok: bool
  transaction: Transaction