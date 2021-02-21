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

    @staticmethod
    def getDevice(deviceName):
        deviceHold = Query()
        result = db.search(deviceHold.name == deviceName)
        deviceHold = LocalControl()
        device = deviceHold.Device(result)
        return device

    async def updateDevice(deviceObject,token,session):
        #update device status in DB
        api = SmartThings(session, token)
        deviceId = deviceObject.device_id
        devices = await api.devices()
        deviceHold = Query()
        for device in devices:
            if device.device_id == deviceObject.device_id:
                if 'switch' in device.capabilities:
                    await device.status.refresh()
                    state = device.status.values['switch']
                    db.update({'state': state}, deviceHold.device_id == deviceId)
        localControl = LocalControl()
        nameN = deviceObject.name
        deviceOut = localControl.getDevice(nameN)
        return deviceOut

    async def toggleDevice(deviceObject, token, session):
        api = SmartThings(session, token)
        deviceId = deviceObject.device_id
        devices = await api.devices()
        deviceHold = Query()
        #db.search(deviceHold.device_id == deviceId)
        for device in devices:
            if device.device_id == deviceId:
                if deviceObject.state == 'on':
                    print('turning off')
                    await device.command("main", "switch", "off")
                    db.update({'state' : 'off'},deviceHold.device_id == deviceId )
                if deviceObject.state == 'off':
                    print('turning on')
                    await device.command("main", "switch", "on")
                    db.update({'state': 'on'}, deviceHold.device_id == deviceId)

    class Device:
        def __init__(self, device):
            self.device_id = device[0]['device_id']
            self.name = device[0]['name']
            self.label = device[0]['label']
            self.capabilities = device[0]['capabilities']
            if device[0]['state']:
                #handle device state
                self.state = device[0]['state']
            else:
                self.state = "NULL"

