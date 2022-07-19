from typing import Dict, Any

from feegee import APP

@APP.get("/v1/definitions/set")
async def definition_set(data: Dict[str, Any]):
