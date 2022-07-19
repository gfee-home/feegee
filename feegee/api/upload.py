from typing import Dict, Any

from feegee import APP

@APP.get("/v1/upload/single")
async def upload_single(data: Dict[str, Any]):
    


