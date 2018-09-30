"""

This Molotov script has 2 scenario

"""
from molotov import scenario
import os


PORT = os.environ.get('MOLOTOV_PORT')


if not PORT:
    raise Exception('Set service port to MOLOTOV_PORT env variable!')

_API = 'http://192.168.99.100:{}/'.format(PORT)


@scenario(weight=40)
async def scenario_one(session):
    async with session.post(_API,
     data='{"v1":3, "v2":2}',
	 headers={'content-type': 'application/json'}
     ) as resp:
        res = await resp.json()
        assert resp.status == 200
