# -*- coding: utf-8 -*-
# @Author  : Qliangw
# @Time    : 2022/3/16 10:57
# @Function:
from enum import Enum

# property type
# "title", "rich_text", "number", "select", "multi_select",
# "date", "people", "files", "checkbox", "url", "email",
# "phone_number", "formula", "relation", "rollup",
# "created_time", "created_by", "last_edited_time", "last_edited_by".

class DatabaseProperty(Enum):
    TITLE = "title"
    RICH_TEXT = "rich_text"
    NUMBER = "number"
    SELECT = "select"
    MULTI_SELECT = "multi_select"
    DATE = "date"
    PEOPLE = "people"
    FILES = "files"
    CHECKBOX = "checkbox"
    URL = "url"
    EMAIL = "email"
    PHONE_NUMBER = "phone_number"
    FORMULA = "formula"
    RELATION = "relation"
    ROLLUP = "rollup"
    CREATED_TIME = "created_time"
    CREATED_BY = "created_by"
    LAST_EDITED_TIME = "last_edited_time"
    LAST_EDITED_BY = "last_edited_by"