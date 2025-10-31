# Fragment API
First open-source Fragment RESTful API for buying Telegram Stars via [Fragment](https://fragment.com)

## Requirements
Fragment authorization cookies. Only accounts with KYC.  
To copy cookies use [Cookie-Editor](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm_) extension.

## How to use
1. Install dependencies:
```bash
   pip install -r requirements.txt
```

2. Create `cookies.json` file and paste there cookies from Fragment:
```json
{
   "stel_dt": "-120",
   "stel_ssid": "YOUR_STEL_SSID_COOKIE",
   "stel_token": "YOUR_STEL_TOKEN_COOKIE",
   "stel_ton_token": "YOUR_STEL_TON_TOKEN_COOKIE"
}
```

3. Start FastAPI server:
```bash
python -m uvicorn main:app
```
