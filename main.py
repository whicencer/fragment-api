from fastapi import FastAPI
from routers import recipients, payments
from fragment.api import FragmentAPI

app = FastAPI(
  title='Fragment API',
  description=f'''
  Github: [https://github.com/whicencer/fragment-api](https://github.com/whicencer/fragment-api)\n
  Contact developer: [https://t.me/whicencer](https://t.me/whicencer)
  '''
)

@app.on_event('startup')
def startup_event():
  app.state.fragment_api = FragmentAPI()

app.include_router(recipients.router)
app.include_router(payments.router)