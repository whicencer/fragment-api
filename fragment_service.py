import requests
from bs4 import BeautifulSoup
import re
import json
import logging

COOKIES_FILE = './cookies.json'

def http_request(url, method='GET', body=None, cookies=None):
  method = method.upper()
  if method not in ('GET', 'POST'):
    raise ValueError('Only POST and GET methods!')

  response = None
  try:
    if method == "GET":
      response = requests.get(url, cookies=cookies)
    else:
      response = requests.post(url, data=body, cookies=cookies)
  except requests.RequestException as e:
    logging.error(f'Error making request: {e}')
  return response

class FragmentAPI:
  def __init__(self):
    self.api_url = f'https://fragment.com'
    self._setup_cookies()
    self._setup_client_data()
  
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
        if state.get('tonRate') is not None:
          self.api_url = self.api_url + api_url
          self.ton_rate = state.get('tonRate')
    except Exception as error:
      print(f'Unexpected error: {error}')
  
  def _setup_cookies(self):
    cookies = {}
    try:
      with open(COOKIES_FILE, 'r') as f:
        cookies = json.load(f)
        self.cookies = cookies
    except:
      raise Exception('Error setting credentials.')
  
  def _fragment_initBuyStarsRequest(self, recipient_id, quantity):
    try:
      response = http_request(
        self.api_url,
        method='POST',
        body={
          'recipient': recipient_id,
          'quantity': quantity,
          'method': 'initBuyStarsRequest'
        },
        cookies=self.cookies
      )
      data = response.json()
      req_id = data.get('req_id')
      if req_id is not None:
        return {
          'req_id': req_id,
          'to_bot': data.get('to_bot'),
          'ton_amount': data.get('amount')
        }
      return None
    except Exception as error:
      print(f'Unexpected error: {error}')
      return None
  
  def _fragment_getBuyStarsLink(self, account, req_id):
    try:
      response = http_request(
        self.api_url,
        method='POST',
        body={
          'account': account,
          'transaction': '1',
          'id': req_id,
          'show_sender': '0',
          'method': 'getBuyStarsLink'
        },
        cookies=self.cookies
      )
      data = response.json()
      transaction = data.get('transaction')
      if transaction:
        del transaction['from']
        return transaction
      return None
    except Exception as error:
      print(f'Unexpected error: {error}')
      return None
  
  def search_stars_recipient(self, recipient_username):
    try:
      response = http_request(
        self.api_url,
        method='POST',
        body={
          'query': recipient_username,
          'quantity': '',
          'method': 'searchStarsRecipient'
        },
        cookies=self.cookies
      )
      data = response.json()
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
      print(f'Unexpected error: {error}')
      return None
  
  def create_stars_transaction(self, recipient_id, quantity, wallet_account):
    try:
      init_buy = self._fragment_initBuyStarsRequest(
        recipient_id=recipient_id,
        quantity=quantity
      )
      
      if init_buy is not None:
        req_id = init_buy.get('req_id')
        if req_id is not None:
          buy_transaction = self._fragment_getBuyStarsLink(
            account=wallet_account,
            req_id=req_id
          )
          return buy_transaction
      return None
    except Exception as error:
      print(f'Unexpected error: {error}')
      return None
  
  def get_ton_rate(self):
    return self.ton_rate