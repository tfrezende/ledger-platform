from collections.abc import AsyncGenerator

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from application.ports.account_repo import AccountRepo
from infrastructure.db.account_repo import SqlAccountRepo


async def get_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    async with request.app.state.session_factory() as session:
        async with session.begin():
            yield session

async def get_account_repo(
    session: AsyncSession = Depends(get_session)
) -> AsyncGenerator[AccountRepo, None]:
    yield SqlAccountRepo(session)
    