from fastapi import Request
from fragment.api import FragmentAPI


def get_fragment_api(request: Request) -> FragmentAPI:
  """Return the shared FragmentAPI instance stored on app.state.

  Place this helper in a central module and import it in routers to avoid
  duplicating the function in every router.
  """
  return request.app.state.fragment_api
