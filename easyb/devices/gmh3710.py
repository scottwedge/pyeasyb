#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
#    Copyright (C) 2017, Kai Raphahn <kai.raphahn@laburec.de>
#

import easyb

from typing import List
from datetime import datetime

from easyb.definitions import Length
from easyb.command import Command
from easyb.device import Device
from easyb.bit import convert_u16

__all__ = [
    "Data",
    "GMH3710"
]

name = "GMH 3710"
device = "GMH3710"


class Data:

    @property
    def datetime(self) -> datetime:
        return self._datetime

    @property
    def value(self) -> float:
        return self._value

    def __init__(self, value: float):
        self._datetime = datetime.now()
        self._value = value
        return


class GMH3710(Device):

    system_state = 0
    min_value = 0.0
    max_value = 0.0
    id_number = 0

    @property
    def data(self) -> List[Data]:
        return self._data

    def __init__(self, **kwargs):
        Device.__init__(self, name="GMH 3710", **kwargs)

        self._data = []
        return

    def messwert_lesen(self) -> bool:
        command = self.get_command(0)

        message = self.execute(command)
        if message is None:
            return False

        if message.length is Length.Byte6:
            message.value_16()

        if message.length is Length.Byte9:
            message.value_32()

        if message.value is None:
            easyb.log.warn(self.name, "No value!")
            return False

        data = Data(message.value)

        debug = "{0:s}: {1:.2f}".format(data.datetime.strftime("%Y-%m-%d %H:%M:%S"), data.value)
        easyb.log.inform(self.name, debug)

        self.data.append(data)
        return True

    def systemstatus_lesen(self) -> bool:
        command = self.get_command(1)

        message = self.execute(command)
        if message is None:
            return False

        message.decode_16()

        easyb.log.inform(self.name, str(message.value))
        self.system_state = int(message.value)
        return True

    def minwert_lesen(self) -> bool:
        command = self.get_command(2)

        message = self.execute(command)
        if message is None:
            return False

        if message.length is Length.Byte6:
            message.value_16()

        if message.length is Length.Byte9:
            message.value_32()

        if message.value is None:
            easyb.log.warn(self.name, "No value!")
            return False

        easyb.log.inform(self.name, str(message.value))
        self.min_value = message.value
        return True

    def maxwert_lesen(self) -> bool:
        command = self.get_command(3)

        message = self.execute(command)
        if message is None:
            return False

        if message.length is Length.Byte6:
            message.value_16()

        if message.length is Length.Byte9:
            message.value_32()

        if message.value is None:
            easyb.log.warn(self.name, "No value!")
            return False

        easyb.log.inform(self.name, str(message.value))
        self.max_value = message.value
        return True

    def id_nummer_lesen(self) -> bool:
        command = self.get_command(4)

        message = self.execute(command)
        if message is None:
            return False

        message.decode_32()

        self.id_number = message.value

        easyb.log.inform(self.name, "ID: {0:x}".format(self.id_number))
        return True

    def anzeige_einheit_lesen(self) -> bool:
        command = self.get_command(9)

        message = self.execute(command)
        if message is None:
            return False

        value = convert_u16(message.data[3], message.data[4])
        easyb.log.inform(self.name, str(value))
        return True

    def init_commands(self):

        command = Command(name="Messwert lesen", number=0, address=self.address, code=0,
                          func_call=self.messwert_lesen)
        self.add_command(command)

        command = Command(name="Systemstatus lesen", number=1, address=self.address, code=3,
                          func_call=self.systemstatus_lesen)
        self.add_command(command)

        command = Command(name="Minwert lesen", number=2, address=self.address, code=6, func_call=self.minwert_lesen)
        self.add_command(command)

        command = Command(name="Maxwert lesen", number=3, address=self.address, code=7, func_call=self.maxwert_lesen)
        self.add_command(command)

        command = Command(name="ID-Nummer lesen", number=4, address=self.address, code=12,
                          func_call=self.id_nummer_lesen)
        self.add_command(command)

        command = Command(name="Anzeige Einheit lesen", number=9, address=self.address, code=15, length=Length.Byte6,
                          param=[202, 0], func_call=self.anzeige_einheit_lesen)
        self.add_command(command)
        return

    def prepare(self) -> bool:
        easyb.log.warn(self.name, "Need to implement!")
        return True

    def run(self) -> bool:
        command = self.get_command(0)

        message = self.execute(command)
        if message is None:
            return False

        self.data.append(Data(message.value))
        return True

    def close(self) -> bool:
        return True
