from fastapi import FastAPI
from routers import recipients, payments
from fragment_service import FragmentAPI

app = FastAPI(title='Fragment API', description='Hello')

@app.on_event('startup')
def startup_event():
  app.state.fragment_api = FragmentAPI()

app.include_router(recipients.router)
app.include_router(payments.router)