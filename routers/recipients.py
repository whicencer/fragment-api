from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fragment_service import FragmentAPI
from dependencies import get_fragment_api
from schemas.SearchRecipient import SearchRecipientDto, SearchRecipientResponse


router = APIRouter(
  prefix='/recipients',
  responses={404: {'description': 'Not found'}},
  tags=['Recipients']
)


@router.post('/stars', response_model=SearchRecipientResponse)
async def searchRecipient(dto: SearchRecipientDto, fragmentApi: FragmentAPI = Depends(get_fragment_api)) -> SearchRecipientResponse:
  try:
    recipient = fragmentApi.search_stars_recipient(recipient_username=dto.username)
    if recipient is None:
      return JSONResponse({ 'ok': False, 'error': 'Recipient not found.' })
    
    return SearchRecipientResponse(
      ok=True,
      recipient_id=recipient.get('recipient_id'),
      name=recipient.get('name'),
      photo=recipient.get('photo')
    )
  except Exception as error:
    print(error)
    return JSONResponse({ 'ok': False, 'error': 'Error occured.' })