from dataclasses import dataclass
from enum import Enum
from typing import List


@dataclass
class TopicTag:
    name: str
    nameTranslated: str


class Difficulty(Enum):
    Easy = 1
    Medium = 2
    Hard = 3

    @classmethod
    def of(cls, type_str: str):
        type_str = type_str.capitalize()
        if type_str in cls._member_names_:
            return cls[type_str]
        else:
            raise Exception("未知类型", type_str)

    def __cmp__(self, other):
        if self.__class__ is other.__class__:
            return self.value - other.value
        return NotImplemented

    def __repr__(self):
        return self.name


@dataclass
class Question:
    title: str
    titleCn: str
    frontendQuestionId: str
    titleSlug: str
    topicTags: List[TopicTag]
    difficulty: Difficulty
    acRate: float
