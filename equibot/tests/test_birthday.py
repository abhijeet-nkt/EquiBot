import pytest
import datetime

from .fixtures import delete_db
from ..repository import Repository

GUILD_ID = 55
GUILD2_ID = 65
CAL_CHAN = 21
GREET_CHAN = 22
USER1 = 77
USER2 = 78

@pytest.mark.asyncio()
async def test_birthdays():
    repo = Repository('_test.db')

    assert await repo.get_birthday_channels(GUILD_ID) == None
    assert await repo.get_birthday_kids() == None

    await repo.set_birthday_channels(GUILD_ID, CAL_CHAN, GREET_CHAN)
    chans = await repo.get_birthday_channels(GUILD_ID)
    assert chans[0] == CAL_CHAN
    assert chans[1] == GREET_CHAN

    date = datetime.datetime.utcnow()
    await repo.set_birthdate(USER1, date.month, date.day)

    assert len(list(await repo.get_birthday_kids())) == 1
    assert list((await repo.get_birthday_kids()))[0] == USER1

    await repo.set_birthdate(USER2, date.month, date.day)
    assert USER2 in (await repo.get_birthday_kids())
    assert USER1 in (await repo.get_birthday_kids())

@pytest.mark.asyncio()
async def test_birthday_completion():
    repo = Repository('_test.db')

    assert not await repo.has_greeted_today()
    await repo.update_greet_completion_date()

    assert await repo.has_greeted_today()

    del repo
    repo = Repository('_test.db')
    assert await repo.has_greeted_today()

@pytest.mark.asyncio()
async def test_birthday_calendar():

    repo = Repository('_test.db')

    assert await repo.get_calendar_message_ids(GUILD_ID) == None

    ids = (5, 6, 7, 5, 6, 7, 3, 66, 700, 900, 55, 7)
    await repo.update_calendar_message_ids(GUILD_ID, ids)
    assert await repo.get_calendar_message_ids(GUILD_ID) == ids

    ids = ids[::-1]
    await repo.update_calendar_message_ids(GUILD_ID, ids)
    assert await repo.get_calendar_message_ids(GUILD_ID) == ids

@pytest.mark.asyncio()
async def test_bithday_ping_roles():

    ROLE_ID1, ROLE_ID2  = 56, 64

    repo = Repository('_test.db')

    assert await repo.get_birthday_ping_role(GUILD_ID) == None
    assert await repo.get_birthday_ping_role(GUILD2_ID) ==  None

    await repo.set_bithday_ping_role(GUILD_ID, ROLE_ID1)
    await repo.set_bithday_ping_role(GUILD2_ID, ROLE_ID2)

    assert await repo.get_birthday_ping_role(GUILD2_ID) == ROLE_ID2
    assert await repo.get_birthday_ping_role(GUILD_ID) == ROLE_ID1

    await repo.set_bithday_ping_role(GUILD_ID, ROLE_ID2)
    await repo.set_bithday_ping_role(GUILD2_ID, ROLE_ID1)

    assert await repo.get_birthday_ping_role(GUILD2_ID) == ROLE_ID1
    assert await repo.get_birthday_ping_role(GUILD_ID) == ROLE_ID2