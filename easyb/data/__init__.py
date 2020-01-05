#!/usr/bin/python3
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

from datetime import datetime

from typing import List, Any

__all__ = [
    "base",

    "Data"
]

from easyb.data.base import Type, Column, Row


class Data:

    rows: List[Row] = []
    columns: List[Column] = []
    counter: int = 0

    @property
    def len(self) -> int:
        result = len(self.rows)
        return result

    def get_column(self, name: str) -> Column:

        column = None

        for item in self.columns:
            if item.name == name:
                column = item

        if column is None:
            raise ValueError("Column {0:s} not found!".format(name))

        return column

    def add_column(self, name: str, desc: str, column_type: Type) -> bool:
        for item in self.columns:
            if item.name == name:
                easyb.log.error("Column with name {0:s} already exists!".format(name))
                return False

        column = Column(self.counter, name, desc, column_type)
        self.columns.append(column)

        self.counter += 1
        return True

    def create_row(self) -> Any:
        key_list = []
        value_list = []

        for column in self.columns:
            key_list.append(column.name)

            value = None

            if column.type is Type.datetime:
                value = datetime.now()

            if column.type is Type.float:
                value = 0.0

            if column.type is Type.integer:
                value = 0

            if column.type is Type.string:
                value = ""

            if value is None:
                return None

            value_list.append(value)

        row = Row(key_list, value_list)
        self.rows.append(row)
        return row


