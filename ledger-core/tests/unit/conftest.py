from __future__ import annotations

import uuid
from datetime import datetime, timezone

import pytest

from domain.account import Account, AccountStatus


@pytest.fixture
def sample_account() -> Account:
    return Account(
        id=uuid.uuid4(),
        owner_id=uuid.uuid4(),
        currency="USD",
        status=AccountStatus.ACTIVE,
        created_at=datetime.now(timezone.utc),
    )
