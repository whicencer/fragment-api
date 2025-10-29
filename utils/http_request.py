import requests

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
    print(f'Error making request: {e}')
  return response