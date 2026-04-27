import asyncio

import uvicorn

from application.fastapi_application.application import app


async def main() -> None:
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    asyncio.run(main())
