from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from schemas.CreateTransaction import CreateTransactionDto, CreateTransactionResponse
from dependencies import get_fragment_api
from fragment.api import FragmentAPI


router = APIRouter(
  prefix='/payments',
  responses={404: {'description': 'Not found'}},
  tags=['Payments']
)


@router.post('/stars', response_model=CreateTransactionResponse)
async def create_transaction(dto: CreateTransactionDto, fragmentApi: FragmentAPI = Depends(get_fragment_api)):
  try:
    transaction = fragmentApi.create_stars_transaction(
      recipient_id=dto.recipient_id,
      quantity=dto.quantity,
      wallet_account=dto.account
    )
    if error := transaction.get('error'):
      return JSONResponse({ 'ok': False, 'error': error })
    
    return CreateTransactionResponse(
      ok=True,
      transaction=transaction
    )
  except Exception as error:
    print(f'Unexpected error occured: {error}')
    return JSONResponse({ 'ok': False, 'error': "Error occured." })

@router.get('/tonRate')
async def get_ton_rate(fragmentApi: FragmentAPI = Depends(get_fragment_api)):
  ton_rate = fragmentApi.get_ton_rate()
  return JSONResponse({ 'ok': True, 'ton_rate': ton_rate })