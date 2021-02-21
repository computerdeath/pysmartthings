import aiohttp
import pysmartthings
from pysmartthings import LocalControl
import asyncio
import sqlite3

def getToken():
    token_file = open('token.key','r')
    token = token_file.read().strip()
    token_file.close()
    return token

async def intializeDB(token):
    async with aiohttp.ClientSession() as session:
        receive = await pysmartthings.LocalControl.intializeDevices(session, token)

def getDevice(deviceName):
    deviceHold = LocalControl
    device = deviceHold.getDevice(deviceName)
    return device

async def toggle(device, token):
    async with aiohttp.ClientSession() as session:
        await LocalControl.toggleDevice(device, token, session)

async def update(device, token):
    async with aiohttp.ClientSession() as session:
        returnDevice = await LocalControl.updateDevice(device, token , session)
    print(returnDevice.name)

if __name__ == "__main__":
    token = getToken()
    #intialize DB
    asyncio.run(intializeDB(token))
    device = getDevice('test')
    print(device.device_id)
    asyncio.run(toggle(device,token))
    asyncio.run(update(device,token))
