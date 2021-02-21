from .smartthings import SmartThings
import aiohttp
from tinydb import TinyDB, Query
from tinydb.operations import set
import asyncio

db = TinyDB('test.json')
class LocalControl:

    async def intializeDevices(session,token):
            api = SmartThings(session, token)
            # clear state of db
            db.truncate()
            devices = await api.devices()
            for device in devices:
                if 'switch' in device.capabilities:
                    await device.status.refresh()
                    state = device.status.values['switch']
                    db.insert({'device_id': device.device_id, 'name': device.name, 'label': device.label, 'capabilities': device.capabilities, 'state' : state})
                else:
                    db.insert({'device_id': device.device_id, 'name': device.name, 'label': device.label, 'capabilities': device.capabilities})

    def getDevice(deviceName):
        deviceHold = Query()
        result = db.search(deviceHold.name == deviceName)
        return result

    async def toggleDevice(deviceObject, token, session):
        api = SmartThings(session, token)
        deviceId = deviceObject[0]['device_id']
        devices = await api.devices()
        deviceHold = Query()
        #db.search(deviceHold.device_id == deviceId)
        for device in devices:
            if device.device_id == deviceId:
                if deviceObject[0]['state'] == 'on':
                    print('turning off')
                    await device.command("main", "switch", "off")
                    db.update({'state' : 'off'},deviceHold.device_id == deviceId )
                if deviceObject[0]['state'] == 'off':
                    print('turning on')
                    await device.command("main", "switch", "on")
                    db.update({ 'state' : 'on'},deviceHold.device_id == deviceId)

