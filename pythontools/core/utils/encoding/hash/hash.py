#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   hash.py
@Date       :   2024/08/12
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/08/12
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""
# here put the import lib

from abc import ABC, abstractmethod


class Hash(ABC):
    @abstractmethod
    @classmethod
    def hash(cls, data: bytes | str) -> int: ...


class Hash128(Hash):
    @classmethod
    def hash(cls, data: bytes | str) -> int:
        return cls.hash_128(data)

    @abstractmethod
    @classmethod
    def hash_128(cls, data: bytes | str) -> int: ...


class Hash64(Hash):
    @classmethod
    def hash(cls, data: bytes | str) -> int:
        return cls.hash_64(data)

    @abstractmethod
    @classmethod
    def hash_64(cls, data: bytes | str) -> int: ...


class Hash32(Hash):
    @classmethod
    def hash(cls, data: bytes | str) -> int:
        return cls.hash_32(data)

    @abstractmethod
    @classmethod
    def hash_32(cls, data: bytes | str) -> int: ...
