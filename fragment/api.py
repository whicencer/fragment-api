from bs4 import BeautifulSoup
from fragment.methods import FragmentMethod
from utils.http_request import http_request
import re
import json

COOKIES_FILE = './cookies.json'

class FragmentAPI:
  def __init__(self):
    self.api_url = f'https://fragment.com'
    self._setup_cookies()
    self._setup_client_data()
  
  def _setup_cookies(self):
    cookies = {}
    try:
      with open(COOKIES_FILE, 'r') as f:
        cookies = json.load(f)
        self.cookies = cookies
    except:
      raise Exception('Error setting cookies.')
  
  def _setup_client_data(self):
    try:
      response = http_request(self.api_url, method='GET', cookies=self.cookies)
      html_content = response.text
      
      soup = BeautifulSoup(html_content, 'html.parser')
      script_tags = soup.find_all('script')
      match = re.search(r'ajInit\(({.+?})\);', html_content)
      
      if match:
        json_str = match.group(1)
        json_obj = json.loads(json_str)
        api_url = json_obj.get('apiUrl')
        state = json_obj.get('state')
        self.api_url = self.api_url + api_url
        self.ton_rate = state.get('tonRate') or None
    except Exception as error:
      print(f'Unexpected error in _setup_client_data: {error}')
  
  def _send_fragment_request(self, method, body):
    if method not in {m.value for m in FragmentMethod}:
      raise ValueError('Unknown method')
    try:
      response = http_request(
        self.api_url,
        method='POST',
        body={
          **(body or {}),
          "method": method
        },
        cookies=self.cookies
      )
      data = response.json()
      return data
    except error:
      print(f'Error in _send_fragment_request: {error}')
      return None
  
  def _initBuyStarsRequest(self, recipient_id, quantity):
    try:
      data = self._send_fragment_request(
        method=FragmentMethod.INIT_BUY_STARS.value,
        body={
          'recipient': recipient_id,
          'quantity': quantity
        }
      )
      req_id = data.get('req_id')
      if req_id is not None:
        return {
          'req_id': req_id,
          'to_bot': data.get('to_bot'),
          'ton_amount': data.get('amount')
        }
      return None
    except Exception as error:
      print(f'Unexpected error in _initBuyStarsRequest: {error}')
      return None
  
  def _getBuyStarsLink(self, account, req_id):
    try:
      data = self._send_fragment_request(
        method=FragmentMethod.GET_BUY_STARS_LINK.value,
        body={
          'account': account,
          'transaction': '1',
          'id': req_id,
          'show_sender': '0'
        }
      )
      transaction = data.get('transaction')
      if isinstance(transaction, dict):
        transaction.pop('from', None)
        return transaction
      return None
    except Exception as error:
      print(f'Unexpected error _getBuyStarsLink: {error}')
      return None
  
  def search_stars_recipient(self, recipient_username):
    try:
      data = self._send_fragment_request(
        method=FragmentMethod.SEARCH_STARS_RECIPIENT.value,
        body={
          'query': recipient_username,
          'quantity': ''
        }
      )
      found = data.get('found')
      
      if found is not None:
        photo = found.get('photo')
        match = re.search(r'src=["\'](.*?)["\']', photo or '')
        photo_src = match.group(1) if match else None
      
      if data.get('ok'):
        return {
          'recipient_id': found.get('recipient'),
          'name': found.get('name'),
          'photo': photo_src
        }
      return None
    except Exception as error:
      print(f'Unexpected error in search_stars_recipient: {error}')
      return None
  
  def create_stars_transaction(self, recipient_id, quantity, wallet_account):
    try:
      init_buy = self._initBuyStarsRequest(
        recipient_id=recipient_id,
        quantity=quantity
      )
      
      if init_buy is not None:
        req_id = init_buy.get('req_id')
        if req_id is not None:
          buy_transaction = self._getBuyStarsLink(
            account=wallet_account,
            req_id=req_id
          )
          return buy_transaction
      return None
    except Exception as error:
      print(f'Unexpected error in create_stars_transaction: {error}')
      return None
  
  def get_ton_rate(self):
    return self.ton_rate