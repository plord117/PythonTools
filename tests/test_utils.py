#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   test_utils.py
@Date       :   2024/07/23
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/07/23
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""
# here put the import lib

import inspect
import random
import re
from datetime import date, datetime, timedelta

import pytest
from loguru import logger

from .context import (
    BasicConvertor,
    BooleanUtil,
    CollectionUtil,
    ConversionError,
    DatetimeUtil,
    DatetimeValidator,
    DesensitizedUtil,
    IDCardUtil,
    PatternPool,
    RadixUtil,
    RandomUtil,
    ReUtil,
    SequenceUtil,
    StringUtil,
    StringValidator,
    TimeUnit,
    TypeUtil,
    ValidationError,
)


class BaseTest:
    TEST_ROUND = 100


class TestStringUtil:
    @classmethod
    def test_equals(cls):
        s1 = None
        s2 = None
        assert StringUtil.equals(s1, s2)

    @classmethod
    def test_is_blank(cls):
        assert StringUtil.is_blank(None)
        assert StringUtil.is_blank("")
        assert StringUtil.is_blank(" \t\n")
        assert not StringUtil.is_blank("abc")

    @classmethod
    def test_all_blank(cls):
        pass

    @classmethod
    def test_get_str_length(cls):
        s = "hello world, 你好啊"
        assert StringUtil.get_width(s) == 19
        assert StringUtil.get_width("") == 0
        assert StringUtil.get_width(None) == 0
        assert StringUtil.get_width("\t") == 1
        assert StringUtil.get_width("\r") == 1
        assert StringUtil.get_width("\n") == 1
        assert StringUtil.get_width("1234567890") == 10
        assert StringUtil.get_width("你好啊") == 6
        assert StringUtil.get_width("hello world") == 11

    @classmethod
    def test_generate_box_string_from_dict_without_chinese(cls):
        d = {
            0: "James Brown",
            1: "Mary Johnson",
            2: "Patricia Smith",
            3: "Robert Williams",
            4: "Linda Jones",
            5: "Michael Brown",
            6: "Elizabeth Garcia",
            7: "David Martinez",
            8: "Barbara Rodriguez",
            9: "Susan Wilson",
        }
        box_str = StringUtil.generate_box_string_from_dict(d)
        logger.debug("\n" + box_str)

    @classmethod
    def test_generate_box_string_from_dict_with_chinese(cls):
        d = {
            "中文姓名": "李军",
            "英文姓名": "John Smith",
            "年龄": 27,
            "地址": "上海市黄浦区",
            "电话号码": "13987654321",
            "电子邮件": "john.smith@example.com",
            "职业": "软件工程师",
        }

        box_str = StringUtil.generate_box_string_from_dict(d, title="个人信息")
        logger.debug("\n" + box_str)
        logger.debug(StringUtil.get_width("+----------------- 个人信息 ------------+"))

    @classmethod
    def test_align_text(cls) -> None:
        s = "hello world, 你好啊"
        assert StringUtil.align_text(s, align="left") == " hello world, 你好啊"
        assert StringUtil.align_text(s, align="center") == " hello world, 你好啊 "
        assert StringUtil.align_text(s, align="right") == "hello world, 你好啊 "

    @classmethod
    def test_get_annotation_str(cls) -> None:
        s1 = "测试1"
        s2 = "测试2-1\n测试2-2\n测试2-3"
        logger.debug(StringUtil.get_annotation_str(s1))
        logger.debug(StringUtil.get_annotation_str(s2))

    @classmethod
    def test_center(cls) -> None:
        a = StringUtil.get_center_msg("hello world", "=", 40)
        b = StringUtil.get_center_msg("hello world", "=", 1)
        logger.debug(a)
        logger.debug(b)

    @classmethod
    def test_and_all_with_correct_arguments(cls) -> None:
        assert not BooleanUtil.and_all(True, False, False, True)
        assert not BooleanUtil.and_all(False, False, False, False)
        assert BooleanUtil.and_all(True, True, True, True)
        assert not BooleanUtil.and_all(True, 0, True, True, strict_mode=False)
        assert not BooleanUtil.and_all(True, "", True, True, strict_mode=False)

    @classmethod
    def test_and_all_with_incorrect_argumens(cls) -> None:
        with pytest.raises(ValueError):
            BooleanUtil.and_all()

    @classmethod
    def test_or_all_with_correct_arguments(cls) -> None:
        assert BooleanUtil.or_all(True, False, False, True)
        assert not BooleanUtil.or_all(False, False, False, False)
        assert BooleanUtil.or_all(True, True, True, True)
        assert BooleanUtil.or_all(True, 0, True, True, strict_mode=False)
        assert not BooleanUtil.or_all(False, "", False, False, strict_mode=False)

    @classmethod
    def test_or_all_with_incorrect_arguments(cls) -> None:
        with pytest.raises(ValueError):
            BooleanUtil.or_all()

    @classmethod
    def test_resize(cls) -> None:
        lst = [1, 2, 3]
        new_lst = SequenceUtil.resize(lst, -1)
        logger.debug(new_lst)

    def test_validate(self) -> None:
        assert DatetimeValidator.is_valid_birthday("19980424")
        assert not DatetimeValidator.is_valid_birthday("19981424")

    def test_id_valid(self) -> None:
        assert IDCardUtil.is_valid_id_18("110105199804246510")
        assert not IDCardUtil.is_valid_id_18("110105199804246511")

    def test_date_sub(self) -> None:
        now = datetime.now() + timedelta(days=1)
        res = now - datetime.now()
        logger.debug(type(res))

    def test_roman_encode(self) -> None:
        assert StringUtil.equals(StringUtil.roman_encode(7), "VII")
        assert StringUtil.equals(StringUtil.roman_encode(1994), "MCMXCIV")
        assert StringUtil.equals(StringUtil.roman_encode(2020), "MMXX")
        assert StringUtil.equals(StringUtil.roman_encode(37), "XXXVII")

    def test_get_roman_range(self) -> None:
        generator = StringUtil.get_roman_range(1, 7)
        lst = ["I", "II", "III", "IV", "V", "VI"]
        for i, v in enumerate(generator):
            assert StringUtil.equals(v, lst[i])

    def test_roman_decode(self) -> None:
        assert StringUtil.roman_decode("VII") == 7
        assert StringUtil.roman_decode("MCMXCIV") == 1994

    def test_has_blank(self) -> None:
        assert StringUtil.has_blank("")
        assert StringUtil.has_blank(" ")
        assert StringUtil.has_blank("", "s", "b")
        assert not StringUtil.has_blank("s", "b")

    def test_is_all_blank(self) -> None:
        assert StringUtil.is_all_blank("")
        assert StringUtil.is_all_blank(" ")
        assert StringUtil.is_all_blank("", " ", "  ", "\t\n")
        assert not StringUtil.is_all_blank("", "s", "b")
        assert not StringUtil.is_all_blank("s", "b")

    def test_is_surround(self) -> None:
        assert StringUtil.is_surround("hello world", "hello", "world")
        assert not StringUtil.is_surround("hello world", "Hello", "world", case_insensitive=False)
        assert StringUtil.is_surround("hello world", "Hello", "world", case_insensitive=True)

    def test_empty_to_default(self) -> None:
        assert StringUtil.empty_to_default("", "default") == "default"
        assert StringUtil.empty_to_default(" ", "default") == " "
        assert StringUtil.empty_to_default("s", "default") == "s"
        assert StringUtil.empty_to_default(None, "default") == "default"

    @classmethod
    def test_remove_blank(cls) -> None:
        original = " hello world \n hello"
        res = StringUtil.remove_blank(original)
        assert res == "helloworldhello"
        logger.debug(f"{original=}\n{res=}")


class TestDateTimeUtil:
    TEST_ROUND = 10

    @classmethod
    def test_get_random_datetime_with_no_args(cls):
        for _ in range(cls.TEST_ROUND):
            res = DatetimeUtil.get_random_datetime()
            logger.debug(f"{res=}")

    @classmethod
    def test_get_random_datetime_with_no_args_include_tz(cls):
        for _ in range(cls.TEST_ROUND):
            res = DatetimeUtil.get_random_datetime(random_tz=True)
            logger.debug(f"{res=}")

    @classmethod
    def test_get_random_date_with_no_args(cls):
        for _ in range(cls.TEST_ROUND):
            logger.debug(DatetimeUtil.get_random_date())

    @classmethod
    def test_get_random_date_with_one_args(cls):
        start = date(1998, 4, 24)
        for _ in range(cls.TEST_ROUND):
            logger.debug(DatetimeUtil.get_random_date(start))

    @classmethod
    def test_get_random_date_with_two_args(cls):
        start = datetime(1998, 4, 24)
        end = datetime(2021, 4, 24)
        for _ in range(cls.TEST_ROUND):
            logger.debug(DatetimeUtil.get_random_date(start, end))

    @classmethod
    def test_get_random_date_with_wrong_args(cls):
        with pytest.raises(ValueError):
            end = datetime(1998, 4, 24)
            start = datetime(2021, 4, 24)
            logger.debug(DatetimeUtil.get_random_date(start, end))

        with pytest.raises(ValueError):
            start = datetime(1998, 4, 24)
            end = datetime(1998, 4, 24)
            logger.debug(DatetimeUtil.get_random_date(start, end))

    @classmethod
    def test_get_this_year(cls):
        logger.debug(DatetimeUtil.this_year())

    @classmethod
    def test_this_quarter(cls) -> None:
        logger.debug(DatetimeUtil.this_quarter())

    @classmethod
    def test_get_this_month(cls):
        logger.debug(DatetimeUtil.this_month())

    @classmethod
    def test_get_this_day(cls):
        logger.debug(DatetimeUtil.this_day())

    @classmethod
    def test_get_this_hour(cls):
        logger.debug(DatetimeUtil.this_hour())

    @classmethod
    def test_get_this_minute(cls):
        logger.debug(DatetimeUtil.this_minute())

    @classmethod
    def test_get_this_second(cls):
        logger.debug(DatetimeUtil.this_second())

    @classmethod
    def test_get_this_millisecond(cls):
        logger.debug(DatetimeUtil.this_millisecond())

    @classmethod
    def test_get_this_ts(cls):
        logger.debug(DatetimeUtil.this_ts())

    @classmethod
    def test_is_leap_year(cls):
        assert DatetimeUtil.is_leap_year(2024)
        assert not DatetimeUtil.is_leap_year(2025)
        assert not DatetimeUtil.is_leap_year(1900)
        assert not DatetimeUtil.is_leap_year(2100)

    @classmethod
    def test_is_same_quarter(cls):
        for _ in range(cls.TEST_ROUND):
            d1 = DatetimeUtil.get_random_datetime()
            d2 = DatetimeUtil.get_random_datetime()
            res = DatetimeUtil.is_same_quarter(d1, d2)
            logger.debug(f"d1={repr(d1)}, d2={repr(d2)}, {res=}")

    @classmethod
    def test_is_same_year(cls):
        for _ in range(cls.TEST_ROUND):
            d1 = DatetimeUtil.get_random_datetime()
            d2 = DatetimeUtil.get_random_datetime()

            assert DatetimeUtil.is_same_year(d1, d2) == (d1.year == d2.year)

        assert not DatetimeUtil.is_same_year(None, None)

    @classmethod
    def test_is_same_month(cls):
        for _ in range(cls.TEST_ROUND):
            d1 = DatetimeUtil.get_random_datetime()
            d2 = DatetimeUtil.get_random_datetime()

            assert DatetimeUtil.is_same_month(d1, d2) == (d1.year == d2.year and d1.month == d2.month)

        assert not DatetimeUtil.is_same_month(None, None)

    @classmethod
    def test_is_same_week(cls):
        for _ in range(cls.TEST_ROUND):
            d1 = DatetimeUtil.get_random_datetime(datetime(2024, 12, 1), datetime(2024, 12, 15))
            d2 = DatetimeUtil.get_random_datetime(datetime(2024, 12, 1), datetime(2024, 12, 15))
            res = DatetimeUtil.is_same_week(d1, d2)
            logger.debug(f"d1={repr(d1)}, d2={repr(d2)}, {res=}")

    @classmethod
    def test_is_same_day(cls):
        for _ in range(cls.TEST_ROUND):
            d1 = DatetimeUtil.get_random_datetime()
            d2 = DatetimeUtil.get_random_datetime()

            assert DatetimeUtil.is_same_day(d1, d2) == (
                d1.year == d2.year and d1.month == d2.month and d1.day == d2.day
            )
            assert not DatetimeUtil.is_same_day(None, None)

    @classmethod
    def test_get_local_tz(cls) -> None:
        for _ in range(cls.TEST_ROUND):
            logger.debug(DatetimeUtil.get_local_tz())

    @classmethod
    def test_sleep(cls) -> None:
        DatetimeUtil.sleep(1)

    @classmethod
    def test_local_to_utc(cls) -> None:
        for _ in range(cls.TEST_ROUND):
            dt = DatetimeUtil.get_random_datetime()
            utc_dt = DatetimeUtil.local_to_utc(dt)
            logger.debug(f"{dt=}, {utc_dt=}")

        with pytest.raises(TypeError):
            DatetimeUtil.local_to_utc(None)

    @classmethod
    def test_get_utc_now(cls) -> None:
        dt = DatetimeUtil.utc_now()
        logger.debug(f"{dt=}")

    @classmethod
    def test_utc_to_local(cls) -> None:
        dt_utc = DatetimeUtil.utc_now()
        dt_local = DatetimeUtil.utc_to_local(dt_utc, "America/New_York")
        logger.debug(f"{dt_utc=}, {dt_local=}")

        with pytest.raises(TypeError):
            DatetimeUtil.utc_to_local(None, "America/New_York")

    @classmethod
    def test_days_in_month(cls) -> None:
        for i, v in enumerate([31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]):
            if i == 2:
                continue
            assert DatetimeUtil.days_in_month(2024, i + 1) == v

    @classmethod
    def test_get_age(cls):
        dt = datetime(1998, 4, 24)
        res_in_float_format = DatetimeUtil.get_age(dt, use_float_format=True)
        logger.debug(f"{res_in_float_format=}")
        res_in_int_format = DatetimeUtil.get_age(dt, use_float_format=False)
        logger.debug(f"{res_in_int_format=}")

        with pytest.raises(ValueError):
            DatetimeUtil.get_age(None)

        DatetimeUtil.get_age(datetime.now() - timedelta(days=365) + timedelta(days=10))

    @classmethod
    def test_time_unit_convert(cls):
        for i in range(cls.TEST_ROUND):
            duration = i * 1000
            res = DatetimeUtil.nanos_to_millis(duration)
            res_second = DatetimeUtil.nanos_to_seconds(duration * 1000)
            logger.debug(f"{i=}, {res=}, {res_second=}")

    @classmethod
    def test_second_to_time(cls):
        for i in range(cls.TEST_ROUND):
            val = random.randrange(1000, 10000, 1000)
            res = DatetimeUtil.second_to_time(val)
            logger.debug(f"{i=}, {val=}, {res=}")

    @classmethod
    def test_conver_time(cls) -> None:
        value = 1000
        res = DatetimeUtil.conver_time(value, TimeUnit.NANOSECONDS, TimeUnit.MILLISECONDS)
        logger.debug(f"{res=}")
        with pytest.raises(ValueError):
            DatetimeUtil.conver_time(None, TimeUnit.DAYS, TimeUnit.SECONDS)

        with pytest.raises(ValueError):
            DatetimeUtil.conver_time(1000, None, TimeUnit.SECONDS)

        with pytest.raises(ValueError):
            DatetimeUtil.conver_time(1000, TimeUnit.DAYS, None)

    @classmethod
    def test_datetime_to_ISO8601(cls):
        for _ in range(cls.TEST_ROUND):
            dt = DatetimeUtil.get_random_datetime()
            res = DatetimeUtil.datetime_to_ISO8601(dt)
            logger.debug(f"{dt=}, {res=}")

        with pytest.raises(TypeError):
            DatetimeUtil.datetime_to_ISO8601(None)

    @classmethod
    def test_sub_before(cls) -> None:
        s1 = "2024-08-01"
        assert StringUtil.sub_before(s1, "-", False) == "2024"
        assert StringUtil.sub_before(s1, "-", True) == "2024-08"
        assert StringUtil.sub_before(s1, "年", False) == "2024-08-01"
        assert StringUtil.sub_before(None, "", True) == ""
        assert StringUtil.sub_before("", "", True) == ""
        assert StringUtil.sub_before("hello world", "", True) == "hello world"

    @classmethod
    def test_sub_after(cls) -> None:
        s1 = "2024-08-01"
        assert StringUtil.sub_after(s1, "-", False) == "08-01"
        assert StringUtil.sub_after(s1, "-", True) == "01"
        assert StringUtil.sub_before(s1, "年", False) == "2024-08-01"
        assert StringUtil.sub_before(None, "", True) == ""
        assert StringUtil.sub_before("", "", True) == ""
        assert StringUtil.sub_before("hello world", "", True) == "hello world"


class TestIdUtil:
    TEST_ROUND = 10000

    @classmethod
    def test_generate_random_id(cls):
        for _ in range(cls.TEST_ROUND):
            id_str_18 = IDCardUtil.generate_random_valid_id()
            id_str_15 = IDCardUtil.generate_random_valid_id(code_length=15)

            assert IDCardUtil.is_valid_id(id_str_18)
            assert IDCardUtil.is_valid_id(id_str_15)

        with pytest.raises(ValueError):
            IDCardUtil.generate_random_valid_id(code_length=21321)

    @classmethod
    def test_convert_id_18_to_15(cls):
        for _ in range(cls.TEST_ROUND):
            id_str_18 = IDCardUtil.generate_random_valid_id()
            id_str_15 = IDCardUtil.convert_18_to_15(id_str_18)
            assert IDCardUtil.is_valid_id(id_str_15)

    @classmethod
    def test_convert_id_15_to_18(cls):
        for _ in range(cls.TEST_ROUND):
            id_str_15 = IDCardUtil.generate_random_valid_id(code_length=15)
            id_str_18 = IDCardUtil.convert_15_to_18(id_str_15)
            assert IDCardUtil.is_valid_id(id_str_18)

    @classmethod
    def test_generate_random_idcard(cls):
        id_obj = IDCardUtil.generate_random_valid_card()
        logger.debug(id_obj)

    @classmethod
    def test_get_birthday_from_id_with_wrong_args(cls):
        assert IDCardUtil.get_birthday_from_id("") is None
        assert IDCardUtil.get_birthday_from_id(1) is None
        assert IDCardUtil.get_birthday_from_id("1") is None
        assert IDCardUtil.get_birthday_from_id("adac") is None
        assert IDCardUtil.get_birthday_from_id("110105199804246511") is None

    @classmethod
    def test_is_valid_id_18(cls):
        assert IDCardUtil.is_valid_id_18("110105199804246510")
        assert not IDCardUtil.is_valid_id_18("1101051998042465")
        assert not IDCardUtil.is_valid_id_18("a10105199804246510")
        assert not IDCardUtil.is_valid_id_18("110105199813246510")

    @classmethod
    def test_is_valid_id(cls):
        _ = "123456789012345"
        # with pytest.raises(NotImplementedError):
        #     IDCardUtil.is_valid_id(id)


# class TestSysUtil:
#     @classmethod
#     def test_list_file(cls):
#         from pathlib import Path

#         p = Path(__file__).parent.parent
#         res = OsUtil.list_files(p, check_exist=False)
#         logger.debug(res)

#         res = OsUtil.list_files(p, check_exist=True)
#         logger.debug(res)

#     @classmethod
#     def test_is_windows(cls):
#         assert not SysUtil.is_windows_platform()

#     @classmethod
#     def test_is_mac(cls):
#         assert SysUtil.is_mac_platform()

#     @classmethod
#     def test_is_linux(cls):
#         assert not SysUtil.is_linux_platform()

#     @classmethod
#     def test_is_python3(cls):
#         assert SysUtil.is_py3()

#     @classmethod
#     def test_is_python2(cls):
#         assert not SysUtil.is_py2()

#     @classmethod
#     def test_get_system_var(cls):
#         assert "/Users/panchenxi" == SysUtil.get_system_property("HOME")
#         assert "panchenxi" == SysUtil.get_system_property("USER")
#         assert "/bin/zsh" == SysUtil.get_system_property("SHELL")

#         assert SysUtil.get_system_property("dadsdsaadsa", None) is None
#         assert 1 == SysUtil.get_system_property("dadsdsaadsa", 1)
#         assert 1 == SysUtil.get_system_property("dadsdsaadsa", 1, quiet=True)
#         assert 1 == SysUtil.get_system_property("dadsdsaadsa", 1, quiet=False)

#     @classmethod
#     def test_get_system_properties(cls):
#         for k, v in SysUtil.get_system_properties().items():
#             logger.debug(f"k={k}, v={v}")


# class TestOsUtil:
#     @classmethod
#     def test_is_contain_hidden_dir(cls):
#         assert OsUtil.is_contain_ignore("/.git")
#         assert OsUtil.is_contain_ignore(".git")
#         assert OsUtil.is_contain_ignore(".svn/sad/")
#         assert OsUtil.is_contain_ignore("/tmp/__pychache__")
#         assert OsUtil.is_contain_ignore("/tmp/__pychache__/pancx")
#         assert OsUtil.is_contain_ignore("__pycache__")
#         assert not OsUtil.is_contain_ignore("/hidden")
#         assert not OsUtil.is_contain_ignore("hidden")
#         assert not OsUtil.is_contain_ignore("usr/local/")
#         assert not OsUtil.is_contain_ignore("/ust/local/security/")

#     @classmethod
#     def test_is_exist(cls):
#         assert OsUtil.is_exist("")
#         assert OsUtil.is_exist("/")
#         assert OsUtil.is_exist("/tmp")
#         assert OsUtil.is_exist("/Users/")
#         assert not OsUtil.is_exist("dsaddaasawdasdwa")

#     @classmethod
#     def test_is_dir(cls):
#         assert OsUtil.is_dir("")
#         assert OsUtil.is_dir("/")
#         assert OsUtil.is_dir("/tmp")
#         assert OsUtil.is_dir("/Users/panchenxi/Work/project/work/长期项目和学习/python/own/PythonTools")

#         assert not OsUtil.is_dir(
#             "/Users/panchenxi/Work/project/work/长期项目和学习/python/own"
#             "/PythonTools/pythontools/component/basic_utils.py",
#             raise_exception=False,
#         )
#         with pytest.raises(Exception):
#             OsUtil.is_dir("dsaddaasawdasdwa", raise_exception=True)

#     @classmethod
#     def test_is_file(cls):
#         assert not OsUtil.is_file("")
#         assert not OsUtil.is_file("/tmp")
#         assert not OsUtil.is_file(
#             "/Users/panchenxi/Work/project/work/长期项目和学习/python/own/PythonTools/pythontools/core/basicutils.py",
#             raise_exception=False,
#         )

#         with pytest.raises(ValueError):
#             OsUtil.is_file("dsaddaasawdasdwa", raise_exception=True)

#     @classmethod
#     def test_get_file_create_time(cls):
#         p = "/Users/panchenxi/Work/project/work/长期项目和学习/python/own/PythonTools/tests/context.py"
#         OsUtil.get_create_time_in_string_format(p)
#         with pytest.raises(ValueError):
#             OsUtil.get_create_time_in_string_format(p + "dadada", check_exist=True)

#     @classmethod
#     def test_list_dirs(cls):
#         res = OsUtil.list_dirs("/Users/panchenxi/Work/project/work/长期项目和学习/python/own/PythonTools")
#         logger.debug(res)

#         OsUtil.list_dirs(
#             "/Users/panchenxi/Work/project/work/长期项目和学习/python/own/PythonTools",
#             check_exist=True,
#         )

#     @classmethod
#     def test_get_extension_from_path(cls):
#         p = "/Users/panchenxi/Work/project/work/长期项目和学习/python/own/PythonTools/pythontools/component/constant.py"  # noqa: E501
#         extension = OsUtil.get_extension_from_path(p)
#         assert ".py" == extension

#     @classmethod
#     def test_is_match_extension(cls):
#         with pytest.raises(ValueError):
#             OsUtil.is_match_extension(".tm", "")

#         p = "/Users/panchenxi/Work/project/work/长期项目和学习/python/own/PythonTools/tests/context.py"
#         assert OsUtil.is_match_extension(p, "py")
#         assert OsUtil.is_match_extension(p, ".py")

#     @classmethod
#     def test_get_file_from_dir_by_extension(cls):
#         p = "/Users/panchenxi/Work/project/work/长期项目和学习/python/own/PythonTools/pythontools" "/component/"
#         res = OsUtil.get_file_from_dir_by_extension(p, extension="py")
#         logger.debug(res)

#     @classmethod
#     def test_get_last_modify_time_in_seconds(cls) -> None:
#         format_str = OsUtil.get_last_modify_time_in_string_format(__file__)
#         seconds = OsUtil.get_last_modify_time_in_seconds(__file__)
#         milliseconds = OsUtil.get_last_modify_time_in_milliseconds(__file__)
#         nanoseconds = OsUtil.get_last_modify_time_in_nanoseconds(__file__)

#         logger.debug(seconds)
#         logger.debug(milliseconds)
#         logger.debug(nanoseconds)
#         logger.debug(format_str)


class TestValidator:
    @classmethod
    def test_is_general_str(cls):
        s = "seda"
        StringValidator.is_general_string(s)
        with pytest.raises(ValidationError):
            StringValidator.is_general_string("123@", raise_exception=True)

    @classmethod
    def test_is_valid_date(cls):
        assert DatetimeValidator.is_valid_date(2022, 12, 1)
        assert DatetimeValidator.is_valid_date(2024, 2, 29)
        assert DatetimeValidator.is_valid_date(1900, 2, 28)
        assert DatetimeValidator.is_valid_date(2022, 3, 31)
        assert not DatetimeValidator.is_valid_date(2022, 12, 33)
        assert not DatetimeValidator.is_valid_date(2022, 13, 1)
        assert not DatetimeValidator.is_valid_date(2022, 2, 29)
        assert not DatetimeValidator.is_valid_date(1900, 2, 29)
        assert not DatetimeValidator.is_valid_date(0, 1, 1)
        assert not DatetimeValidator.is_valid_date(2022, 4, 31)

    @classmethod
    def test_is_valid_birthday(cls):
        assert DatetimeValidator.is_valid_birthday("20221201")
        assert DatetimeValidator.is_valid_birthday("20240229")
        assert DatetimeValidator.is_valid_birthday("19000228")
        assert not DatetimeValidator.is_valid_birthday("2022331")
        assert DatetimeValidator.is_valid_birthday("2024年4月24日")
        assert not DatetimeValidator.is_valid_birthday("2022131")
        assert not DatetimeValidator.is_valid_birthday("20221233")
        assert not DatetimeValidator.is_valid_birthday("2022229")
        assert not DatetimeValidator.is_valid_birthday("19000229")
        assert not DatetimeValidator.is_valid_birthday("011")
        assert not DatetimeValidator.is_valid_birthday("20220431")


class TestStringValidator:
    TEST_ROUND = 1000

    @classmethod
    def test_is_json_str(cls):
        assert StringValidator.is_json('{"name": "Peter"}')
        assert StringValidator.is_json("[1, 2, 3]")
        assert not StringValidator.is_json("{nope}")
        assert not StringValidator.is_json("nope")
        assert not StringValidator.is_json("")
        assert not StringValidator.is_json(None)

    @classmethod
    def test_is_general_string_with_length(cls):
        static_str = "1234567890"
        assert StringValidator.is_general_string_with_length(static_str, 1, 20)
        assert not StringValidator.is_general_string_with_length(static_str, 1, 2)

        for _ in range(cls.TEST_ROUND):
            random_length = RandomUtil.get_random_val_from_range(1, 20)
            random_str = StringUtil.get_random_strs(random_length)
            random_test_length = RandomUtil.get_random_val_from_range(1, 20)
            if random_test_length >= random_length:
                assert StringValidator.is_general_string_with_length(random_str, 1, random_test_length)
            else:
                assert not StringValidator.is_general_string_with_length(random_str, 1, random_test_length)

    @classmethod
    def test_is_general_string_with_length2(cls):
        static_str = "1234567890"
        assert StringValidator.is_general_string_with_length(static_str, 1, -1)

    @classmethod
    def test_is_money(cls) -> None:
        # PERF 搞清楚这个正则表达式
        assert StringValidator.is_money("456.789")

    @classmethod
    def test_is_zip_code(cls) -> None:
        for test_obj in ["210018", "210001", "210009", "210046"]:
            assert StringValidator.is_zip_code(test_obj)

    @classmethod
    def test_is_mobile(cls) -> None:
        correct_phone = "17161193307"
        incorrect_phone = "1716119330"
        assert StringValidator.is_mobile(correct_phone)
        assert not StringValidator.is_mobile(incorrect_phone)

    @classmethod
    def test_is_email(cls) -> None:
        incorrect_emails = [
            "plainaddress",
            "@missingusername.com",
            "user@.com.my",
            "user@domain..com",
            "user@-domain.com",
        ]

        correct_emails = [
            "user@example.com",
            "firstname.lastname@example.com",
            "user+mailbox@example.com",
            "user.name+tag+sorting@example.com",
            "user@example.co.uk",
            "user_name@example.com",
            "user-name@example.com",
            "user.name@subdomain.example.com",
            "user_name+123@example.com",
            "user@domain.com.",
            "user@123.123.123.123",
            "user@domain-with-dash.com",
            "user@domain-with-dash.com",
            "user@123.123.123.123",
        ]

        for correct_email in correct_emails:
            assert StringValidator.is_email(correct_email)

        for incorrect_email in incorrect_emails:
            assert not StringValidator.is_email(incorrect_email)

    @classmethod
    def test_is_hex(cls) -> None:
        correct_hex = [
            "1A2B3C",  # 常见的十六进制字符串
            "abcdef",  # 小写字母
            "ABCDEF",  # 大写字母
            "123",  # 单一的有效十六进制数字
            "0x123ABC",
            "ff",  # 最小有效的两位十六进制数字
            "7F",  # 一字节的十六进制数值
            "000001",  # 具有前导零的有效十六进制字符串
            "DEADBEEF",  # 经典的十六进制字符串
        ]

        incorrect_hex = [
            "G123",  # 非十六进制字符
            "123Z",  # 非十六进制字符
            "0xGHIJKL",  # 前缀但包含非十六进制字符
            "123ABC!"  # 包含非十六进制字符
            "1.2.3",  # 包含点号的无效格式
            "123 456",  # 包含空格的无效格式
            "",  # 空字符串
            "0x123 456",  # 带有空格的前缀十六进制字符串
        ]

        for correct_str in correct_hex:
            assert StringValidator.is_hex(correct_str)

        for incorrect_str in incorrect_hex:
            assert not StringValidator.is_hex(incorrect_str)

    @classmethod
    def test_is_chinese_vehicle_number(cls) -> None:
        correct_vin = [
            "京A12345",  # 北京市的车牌号
            "沪B23456",  # 上海市的车牌号
            "粤C34567",  # 广东省的车牌号
            "苏D45678",  # 江苏省的车牌号
            "浙E56789",  # 浙江省的车牌号
            "川H12345",  # 四川省的车牌号
            "桂K12345",  # 广西省的车牌号
        ]

        incorrect_vin = [
            "AB12345",  # 无效的车牌号格式（省份代码错误）
            "京123456",  # 车牌号长度超出有效范围
            "粤C3456",  # 车牌号长度不足
            "苏1234",  # 缺少省份代码
            "浙E5678AB",  # 包含无效字符
            "鲁F123456",  # 车牌号长度超出有效范围
            "晋5678",  # 缺少省份代码
            "川H123456",  # 车牌号长度超出有效范围
            "鄂J123",  # 车牌号长度不足
            "桂K1234567",  # 车牌号长度超出有效范围
        ]

        for correct_vin_str in correct_vin:
            assert StringValidator.is_chinese_vehicle_number(correct_vin_str)

        for incorrect_vin_str in incorrect_vin:
            assert not StringValidator.is_chinese_vehicle_number(incorrect_vin_str)

    @classmethod
    def test_get_common_prefix(cls) -> None:
        test_1_str1 = "hello world"
        test_2_str2 = "hello python"
        assert StringUtil.equals(StringUtil.get_common_prefix(test_1_str1, test_2_str2), "hello ")

        test_2_str1 = "programming"
        test_2_str2 = "progress"
        assert StringUtil.equals(StringUtil.get_common_prefix(test_2_str1, test_2_str2), "progr")

        test_3_str1 = "1llo world"
        test_3_str2 = "hello python"
        assert StringUtil.is_blank(StringUtil.get_common_prefix(test_3_str1, test_3_str2))

    @classmethod
    def test_get_common_suffix(cls) -> None:
        test_1_str1 = "hello 我的世界 python"
        test_2_str2 = "hello python"  # 注意：这里的字符串顺序是反的
        assert StringUtil.equals(StringUtil.get_common_suffix(test_1_str1, test_2_str2), " python")

        test_2_str1 = "programming"
        test_2_str2 = "running"
        assert StringUtil.equals(StringUtil.get_common_suffix(test_2_str1, test_2_str2), "ing")

        test_3_str1 = "hello world"
        test_3_str2 = "hello python"
        assert StringUtil.equals(StringUtil.get_common_suffix(test_3_str1, test_3_str2), "")

    @classmethod
    def test_group_by_length(cls) -> None:
        input_string = "abcdefghij"
        result = StringUtil.group_by_length(input_string, 3)
        assert result == ["abc", "def", "ghi", "j"]

    @classmethod
    def test_format_in_currency(cls) -> None:
        assert StringUtil.equals(StringUtil.format_in_currency("123456789"), "123,456,789")
        assert StringUtil.equals(StringUtil.format_in_currency("123456789.45"), "123,456,789.45")
        assert StringUtil.equals(StringUtil.format_in_currency("-123456789.45"), "-123,456,789.45")
        assert StringUtil.equals(StringUtil.format_in_currency("0"), "0")
        assert StringUtil.equals(StringUtil.format_in_currency("-123456789"), "-123,456,789")

    @classmethod
    def test_abbreviate_string(cls) -> None:
        assert StringUtil.abbreviate("abcdefg", 6) == "abc..."
        assert StringUtil.abbreviate(None, 7) == ""  # type: ignore
        assert StringUtil.abbreviate("abcdefg", 8) == "abcdefg"
        assert StringUtil.abbreviate("abcdefg", 4) == "a..."

        with pytest.raises(ValueError):
            StringUtil.abbreviate("abcdefg", 0)


class TestReUtil:
    @classmethod
    def test_is_match_regex(cls):
        assert ReUtil.is_match(re.compile(r"\d+"), "123456")
        words = "...words, words..."
        pattern = re.compile(r"(\W+)")
        assert ReUtil.is_match(pattern, words)
        res = ReUtil.get_group_1(pattern, words)
        logger.debug(f"{res=}")

    @classmethod
    def test_get_group_0(cls):
        birthday = "20221201"
        matched = PatternPool.BIRTHDAY_PATTERN.findall(birthday)
        _ = PatternPool.BIRTHDAY_PATTERN.match(birthday)
        _ = PatternPool.BIRTHDAY_PATTERN.search(birthday)
        res3 = PatternPool.BIRTHDAY_PATTERN.match(birthday)
        _ = res3.groups()
        print(matched)


class TestRadixUtil:
    @classmethod
    def test_decimal_to_any(cls):
        assert RadixUtil.convert_base("1011", 2, 10) == "11"
        assert RadixUtil.convert_base("11", 10, 2) == "1011"
        assert RadixUtil.convert_base("A", 16, 2) == "1010"
        assert RadixUtil.convert_base("1010", 2, 16) == "A"
        assert RadixUtil.convert_base("255", 10, 16) == "FF"
        assert RadixUtil.convert_base("FF", 16, 10) == "255"
        assert RadixUtil.convert_base("10101010", 2, 16) == "AA"
        assert RadixUtil.convert_base("AA", 16, 2) == "10101010"
        assert RadixUtil.convert_base("10101010", 2, 8) == "252"
        assert RadixUtil.convert_base("252", 8, 2) == "10101010"

    @classmethod
    def test_get_lst_one_idx(cls) -> None:
        assert RadixUtil.get_lst_one_idx(3) == 1
        logger.debug(RadixUtil.get_lst_one_idx(1))


class TestBooleanUtil:
    @classmethod
    def test_negate_with_correct_arguments(cls) -> None:
        assert not BooleanUtil.negate(True)
        assert BooleanUtil.negate(False)

    @classmethod
    def test_negate_with_incorrect_arguments(cls) -> None:
        with pytest.raises(TypeError):
            BooleanUtil.negate(1, raise_exception=True)

        assert not BooleanUtil.negate(1, raise_exception=False)

    @classmethod
    def test_negate_with_incorrect_arguments_and_default_value(cls) -> None:
        assert not BooleanUtil.negate(1)
        assert BooleanUtil.negate(0)

    @classmethod
    def test_xor_with_correct_arguments(cls) -> None:
        assert BooleanUtil.xor(True, False)
        assert not BooleanUtil.xor(True, False, True)
        assert BooleanUtil.xor(True, False, False)
        assert not BooleanUtil.xor(True, True)

    @classmethod
    def test_xor_with_incorrect_arguments(cls) -> None:
        with pytest.raises(ValueError):
            BooleanUtil.xor()

    @classmethod
    def test_boolean_to_int_with_correct_arguments(cls) -> None:
        state = True
        assert BooleanUtil.boolean_to_int(state) == 1
        assert BooleanUtil.boolean_to_int(not state) == 0

    @classmethod
    def test_boolean_to_int_with_incorrect_arguments(cls) -> None:
        with pytest.raises(ValueError):
            BooleanUtil.boolean_to_int(1, strict_mode=True) == 1

        assert BooleanUtil.boolean_to_int(1, strict_mode=False) == 1
        assert BooleanUtil.boolean_to_int(1) == 1

    @classmethod
    def test_str_to_boolean(cls) -> None:
        assert not BooleanUtil.str_to_boolean("")
        assert BooleanUtil.str_to_boolean("True")
        assert BooleanUtil.str_to_boolean("对")
        assert BooleanUtil.str_to_boolean("ok")
        assert not BooleanUtil.str_to_boolean("false")
        assert not BooleanUtil.str_to_boolean("no")
        assert not BooleanUtil.str_to_boolean("0")
        assert not BooleanUtil.str_to_boolean("错")
        assert not BooleanUtil.str_to_boolean("×")

    @classmethod
    def test_to_str_true_and_false(cls) -> None:
        assert BooleanUtil.to_str_true_and_false(True) == "TRUE"
        assert BooleanUtil.to_str_true_and_false(False) == "FALSE"

    @classmethod
    def test_to_str_yes_no(cls) -> None:
        assert BooleanUtil.to_str_yes_no(True) == "YES"
        assert BooleanUtil.to_str_yes_no(False) == "NO"


class TestRandomUtil:
    TEST_ROUND = 100

    @classmethod
    def test_get_random_boolean(cls):
        for _ in range(cls.TEST_ROUND):
            assert RandomUtil.get_random_boolean() in [True, False]

    @classmethod
    def test_get_random_val_from_range_with_wrong_arguments(cls):
        with pytest.raises(ValueError):
            RandomUtil.get_random_val_from_range(10, 1)

    @classmethod
    def test_get_random_item_from_sequence(cls):
        sequence = []
        assert RandomUtil.get_random_item_from_sequence(sequence) is None

    @classmethod
    def test_get_random_items_from_sequence_with_correct_arguments(cls):
        empty_sequence = []
        assert RandomUtil.get_random_items_from_sequence(empty_sequence, 1) == []
        sequence = [1, 2, 3, 4, 5]
        random_sequence = RandomUtil.get_random_items_from_sequence(sequence, 3)
        assert SequenceUtil.get_length(random_sequence) == 3

        random_sequence = RandomUtil.get_random_items_from_sequence(sequence, 15)
        assert random_sequence == sequence

    @classmethod
    def test_get_random_items_from_sequence_with_incorrect_arguments(cls):
        sequence = [1, 2, 3, 4, 5]
        with pytest.raises(ValueError):
            RandomUtil.get_random_items_from_sequence(sequence, -1)

    @classmethod
    def test_get_random_booleans(cls):
        for i in RandomUtil.get_random_booleans(5):
            assert isinstance(i, bool)

    @classmethod
    def test_get_random_float(cls):
        for _ in range(cls.TEST_ROUND):
            random_float = RandomUtil.get_random_float()
            assert 0.0 <= random_float <= 1.0 and isinstance(random_float, float)

    @classmethod
    def test_get_random_floats_with_range_and_precision_and_correct_arguments(cls):
        for _ in range(cls.TEST_ROUND):
            random_generator = RandomUtil.get_random_floats_with_range_and_precision(0.0, 1.0, precision=2, length=5)
            for random_float in random_generator:
                assert 0.0 <= random_float <= 1.0 and isinstance(random_float, float)

    @classmethod
    def test_get_random_floats_with_range_and_precision_and_incorrect_arguments(cls):
        for _ in range(cls.TEST_ROUND):
            with pytest.raises(ValueError):
                random_generator = RandomUtil.get_random_floats_with_range_and_precision(
                    1.0, 0.0, precision=2, length=5
                )
                for i in random_generator:
                    pass

    @classmethod
    def test_get_random_complex(cls):
        for _ in range(cls.TEST_ROUND):
            random_complex = RandomUtil.get_random_complex()
            assert isinstance(random_complex, complex)

    @classmethod
    def test_get_random_complexes_with_range_and_precision(cls):
        random_generator = RandomUtil.get_random_complexes_with_range_and_precision((0, 1), (-1, 1))
        lst = list(random_generator)
        assert len(lst) == 10
        for i in random_generator:
            real_part = i.real
            imag_part = i.imag

            assert 0 <= real_part <= 1
            assert -1 <= imag_part <= 1


class TestSequenceUtil(BaseTest):
    @classmethod
    def test_get_chunks(cls) -> None:
        test_seq_1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        chunks = SequenceUtil.get_chunks(test_seq_1, 3)
        assert next(chunks) == [1, 2, 3]
        assert next(chunks) == [4, 5, 6]
        assert next(chunks) == [7, 8, 9]
        with pytest.raises(StopIteration):
            next(chunks)

        test_seq_2 = [1, 2, 3, 4]
        chunks = SequenceUtil.get_chunks(test_seq_2, 3)
        assert next(chunks) == [1, 2, 3]
        assert next(chunks) == [4]
        with pytest.raises(StopIteration):
            next(chunks)

        test_seq_3: list[int] = []
        chunks = SequenceUtil.get_chunks(test_seq_3, 3)
        with pytest.raises(StopIteration):
            next(chunks)

        test_seq_4 = None
        chunks = SequenceUtil.get_chunks(test_seq_4, 3)
        with pytest.raises(ValueError):
            next(chunks)

    @classmethod
    def test_(cls) -> None:
        test_seq_1 = [1, [2, 3], 4, [5, [6, 7]]]
        flatten_lst = SequenceUtil.flatten_sequence(test_seq_1)
        assert list(flatten_lst) == [1, 2, 3, 4, 5, 6, 7]

        test_seq_2 = [1, [2, 3], 4, [5, [6, 7]]]
        flatten_lst = SequenceUtil.flatten_sequence(test_seq_2)
        for i in range(1, 8):
            assert next(flatten_lst) == i

        test_seq_3 = [1, 2, 3, 4, 5]
        flatten_lst = SequenceUtil.flatten_sequence(test_seq_3)
        for i in range(1, 6):
            assert next(flatten_lst) == i

        test_seq_4 = []  # type: ignore
        flatten_lst = SequenceUtil.flatten_sequence(test_seq_4)
        with pytest.raises(StopIteration):
            next(flatten_lst)

        test_seq_5 = None  # type: ignore
        flatten_lst = SequenceUtil.flatten_sequence(test_seq_5)  # type: ignore
        with pytest.raises(TypeError):
            next(flatten_lst)

    @classmethod
    def test_is_not_empty(cls) -> None:
        lst = [1, 2, 3]
        assert SequenceUtil.is_not_empty(lst)
        assert not SequenceUtil.is_not_empty([])

    @classmethod
    def test_reverse_sequence(cls) -> None:
        lst = [1, 2, 3]
        reversed_lst = SequenceUtil.reverse_sequence(lst)
        assert reversed_lst == [3, 2, 1]

    @classmethod
    def test_has_none(cls) -> None:
        assert not SequenceUtil.has_none([1, 2, 3])
        assert SequenceUtil.has_none([1, 2, None])

    @classmethod
    def test_new_list(cls) -> None:
        assert SequenceUtil.new_list(5, 0) == [0, 0, 0, 0, 0]
        assert SequenceUtil.new_list(3) == [None, None, None]

    @classmethod
    def test_contains_any(cls) -> None:
        assert SequenceUtil.contains_any([1, 2, 3], *[2, 3, 4])  # True
        assert not SequenceUtil.contains_any([1, 2, 3], *[4, 5, 6])  # False

    @classmethod
    def test_first_idx_of_none(cls) -> None:
        assert SequenceUtil.first_idx_of_none([1, 2, 3]) == -1
        assert SequenceUtil.first_idx_of_none([1, 2, None]) == 2

    @classmethod
    def test_is_all_ele_equal(cls) -> None:
        assert SequenceUtil.is_all_element_equal([1, 1, 1, 1])  # True
        assert not SequenceUtil.is_all_element_equal([1, 2, 1, 1])  # False

    @classmethod
    def test_move(cls) -> None:
        original_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for _ in range(cls.TEST_ROUND):
            move_length = random.randint(0, 100)
            res = SequenceUtil.rotate(original_list, move_length)
            logger.debug(f"{res=}, {move_length=}, {move_length % len(original_list)=}")


class TestCollectionUtil:
    @classmethod
    def test_powerset(cls):
        s = [1, 2, 3]
        for subset in CollectionUtil.get_powerset(s):
            for j in subset:
                logger.debug(j)

    @classmethod
    def test_nested_dict_iter(cls):
        d = {"a": {"a": {"y": 2}}, "b": {"c": {"a": 5}}, "x": {"a": 6}}
        list(CollectionUtil.nested_dict_iter(d))

    @classmethod
    def test_split_sequence(cls) -> None:
        test_seq = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        assert SequenceUtil.split_sequence(test_seq, 3) == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        assert SequenceUtil.split_sequence(test_seq, 1) == [[1, 2, 3, 4, 5, 6, 7, 8, 9]]
        assert SequenceUtil.split_sequence(test_seq, 10) == [[1], [2], [3], [4], [5], [6], [7], [8], [9]]
        SequenceUtil.split_sequence(test_seq, 4) == [[1, 2], [3, 4], [5, 6], [7, 8, 9]]
        with pytest.raises(ValueError):
            assert SequenceUtil.split_sequence(test_seq, 0) == []

    @classmethod
    def test_split_half(cls) -> None:
        test_seq_1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        assert SequenceUtil.split_half(test_seq_1) == [[1, 2, 3, 4], [5, 6, 7, 8, 9]]
        test_seq_2 = [1, 2, 3, 4, 5, 6, 7, 8]
        assert SequenceUtil.split_half(test_seq_2) == [[1, 2, 3, 4], [5, 6, 7, 8]]


class TestTypeUtil:
    @classmethod
    def test_get_class_names(cls) -> None:
        test_1_obj = MoreDerived()
        res = TypeUtil.get_class_mro(test_1_obj)
        logger.debug(res)

        test_2_obj = Derived
        res = TypeUtil.get_class_mro(test_2_obj)
        logger.debug(res)

    @classmethod
    def test_get_class_tree(cls) -> None:
        res = inspect.getclasstree(MoreDerived())
        logger.debug(res)

    @classmethod
    def test_get_function_info(cls) -> None:
        def test_func(a: int, b: str, c: int = 1, *args, **kwargs):
            pass

        res = TypeUtil.get_function_info(test_func)
        logger.debug(res)

    @classmethod
    def test_show_function_info(cls) -> None:
        TypeUtil.show_function_info(StringUtil.get_common_suffix, show_detail=True)

    @classmethod
    def test_get_class_name(cls) -> None:
        res = TypeUtil.get_class_name(StringUtil)
        logger.debug(res)


class Base:
    pass


class Derived(Base):
    pass


class MoreDerived(Derived, list):
    pass


class TestUtil:
    @classmethod
    def test_desensitize_ipv4(cls) -> None:
        ipv4 = "192.0.2.1"
        assert DesensitizedUtil.desensitize_ipv4(ipv4) == "192.*.*.*"
        assert StringUtil.equals(DesensitizedUtil.desensitize_ipv4(ipv4.encode("utf-8")), "192.*.*.*")

    @classmethod
    def test_desensitize_ipv6(cls) -> None:
        ipv6 = "2001:0db8:86a3:08d3:1319:8a2e:0370:7344"
        assert DesensitizedUtil.desensitize_ipv6(ipv6) == "2001:*:*:*:*:*:*:*"
        assert StringUtil.equals(DesensitizedUtil.desensitize_ipv6(ipv6.encode("utf-8")), "2001:*:*:*:*:*:*:*")

    @classmethod
    def test_desensitize_email(cls) -> None:
        email1 = "duandazhi-jack@gmail.com.cn"
        assert DesensitizedUtil.desensitize_email(email1) == "d*************@gmail.com.cn"
        email2 = "duandazhi@126.com"
        assert StringUtil.equals("d********@126.com", DesensitizedUtil.desensitize_email(email2))
        email3 = "duandazhi@gmail.com.cn"
        assert StringUtil.equals("d********@gmail.com.cn", DesensitizedUtil.desensitize_email(email3))
        assert StringUtil.equals("d********@gmail.com.cn", DesensitizedUtil.desensitize_email(email3.encode("utf-8")))
        assert StringUtil.equals("", DesensitizedUtil.desensitize_email(""))

    @classmethod
    def test_desensitize_id_card(cls) -> None:
        id_card = "51343620000320711X"
        assert DesensitizedUtil.desensitize_id_card(id_card) == "513436********711X"
        assert StringUtil.equals(DesensitizedUtil.desensitize_id_card(id_card.encode("utf-8")), "513436********711X")

    @classmethod
    def test_desensitize_bank_card(cls) -> None:
        bank_card1 = "1234 2222 3333 4444 6789 9"
        assert DesensitizedUtil.desensitize_bank_card(bank_card1) == "1234 **** **** **** **** 9"
        bank_card2 = "1234 **** **** **** **** 91"
        assert DesensitizedUtil.desensitize_bank_card(bank_card2) == "1234 **** **** **** **** 91"
        bank_card3 = "1234 2222 3333 4444 6789"
        assert DesensitizedUtil.desensitize_bank_card(bank_card3) == "1234 **** **** **** 6789"
        bank_card4 = "1234 2222 3333 4444 678"
        assert DesensitizedUtil.desensitize_bank_card(bank_card4) == "1234 **** **** **** 678"
        # bytes
        assert StringUtil.equals(
            DesensitizedUtil.desensitize_bank_card(bank_card3.encode("utf-8")), "1234 **** **** **** 6789"
        )
        assert StringUtil.equals(DesensitizedUtil.desensitize_bank_card(""), "")

    @classmethod
    def test_desensitize_mobile_phone(cls) -> None:
        phone1 = "18049531999"
        assert StringUtil.equals("180****1999", DesensitizedUtil.desensitize_mobile_phone(phone1))
        assert StringUtil.equals("180****1999", DesensitizedUtil.desensitize_mobile_phone(phone1.encode("utf-8")))

    @classmethod
    def test_desensitize_fix_phone(cls) -> None:
        fix_phone1 = "09157518479"
        assert StringUtil.equals("091****8479", DesensitizedUtil.desensitize_fix_phone(fix_phone1))
        assert StringUtil.equals("091****8479", DesensitizedUtil.desensitize_fix_phone(fix_phone1.encode("utf-8")))

    @classmethod
    def test_desensitize_car_license(cls) -> None:
        car_license1 = "苏D40000"
        assert StringUtil.equals("苏D4***0", DesensitizedUtil.desensitize_car_license(car_license1))
        car_license2 = "陕A12345D"
        assert StringUtil.equals("陕A1****D", DesensitizedUtil.desensitize_car_license(car_license2))
        car_license3 = "京A123"
        with pytest.raises(ValueError) as _:
            assert StringUtil.equals("京A123", DesensitizedUtil.desensitize_car_license(car_license3))

        assert StringUtil.equals("陕A1****D", DesensitizedUtil.desensitize_car_license(car_license2.encode("utf-8")))
        assert StringUtil.equals("", DesensitizedUtil.desensitize_car_license(""))

    @classmethod
    def test_desensitize_address(cls) -> None:
        address = "北京市海淀区马连洼街道289号"
        assert StringUtil.equals("北京市海淀区马连洼街*****", DesensitizedUtil.desensitize_address(address, 5))
        assert StringUtil.equals("***************", DesensitizedUtil.desensitize_address(address, 50))
        assert StringUtil.equals("北京市海淀区马连洼街道289号", DesensitizedUtil.desensitize_address(address, 0))
        assert StringUtil.equals("北京市海淀区马连洼街道289号", DesensitizedUtil.desensitize_address(address, -1))
        # butes
        assert StringUtil.equals(
            "北京市海淀区马连洼街道289号", DesensitizedUtil.desensitize_address(address.encode("utf-8"), -1)
        )

    @classmethod
    def test_password(cls) -> None:
        password1 = "password"
        assert StringUtil.equals("********", DesensitizedUtil.desensitize_password(password1))
        assert StringUtil.equals("********", DesensitizedUtil.desensitize_password(password1.encode("utf-8")))

    @classmethod
    def test_desensitize_chineseName(cls) -> None:
        assert StringUtil.equals("段**", DesensitizedUtil.desensitize_chinese_name("段正淳"))
        assert StringUtil.equals("张*", DesensitizedUtil.desensitize_chinese_name("张三"))

    @classmethod
    def test_retain_last(cls) -> None:
        s = "asdasc"
        assert StringUtil.equals("*****c", DesensitizedUtil.retain_last(s))

    @classmethod
    def test_retain_front_and_end(cls) -> None:
        assert StringUtil.equals("", DesensitizedUtil.retain_front_and_end("", 3, 4))
        assert StringUtil.equals("", DesensitizedUtil.retain_front_and_end("  ", 3, 4))
        with pytest.raises(ValueError):
            assert StringUtil.equals("", DesensitizedUtil.retain_front_and_end("sad", 3, 4))

        with pytest.raises(ValueError):
            assert StringUtil.equals("", DesensitizedUtil.retain_front_and_end("sad", 3, -1))

    @classmethod
    def test_desensitize_phone(cls) -> None:
        phone = "18049531999"
        assert StringUtil.equals("180****1999", DesensitizedUtil.desensitize_phone(phone))


class TestConvertor:
    @classmethod
    def test_convert_to_str(cls) -> None:
        assert BasicConvertor.to_str(123) == "123"
        assert BasicConvertor.to_str(123.456) == "123.456"
        assert BasicConvertor.to_str(True) == "True"
        assert BasicConvertor.to_str(False) == "False"
        assert BasicConvertor.to_str(None) == ""
        assert BasicConvertor.to_str("abc") == "abc"
        assert BasicConvertor.to_str([1, 2, 3]) == "123"
        assert BasicConvertor.to_str((1, 2, 3)) == "123"
        assert BasicConvertor.to_str({"a": 1, "b": 2}) == "ab"

    @classmethod
    def test_convert_to_int(cls) -> None:
        assert BasicConvertor.to_int("123") == 123
        assert BasicConvertor.to_int("123.456") == 123
        assert BasicConvertor.to_int(True) == 1
        assert BasicConvertor.to_int(False) == 0
        assert BasicConvertor.to_int(None) == 0
        assert BasicConvertor.to_int("abc") == 0
        assert BasicConvertor.to_int([1, 2, 3]) == 0
        assert BasicConvertor.to_int((1, 2, 3)) == 0
        assert BasicConvertor.to_int({"a": 1, "b": 2}) == 0

        assert BasicConvertor.to_int("123", 100) == 123
        assert BasicConvertor.to_int("abc", 100) == 100
        with pytest.raises(ConversionError):
            BasicConvertor.to_int("sda", raise_exception=True)

    @classmethod
    def test_convert_to_float(cls) -> None:
        assert BasicConvertor.to_float("123") == 123.0
        assert BasicConvertor.to_float("123.456") == 123.456
        assert BasicConvertor.to_float(True) == 1.0
        assert BasicConvertor.to_float(False) == 0.0
        assert BasicConvertor.to_float(None) == 0.0
        assert BasicConvertor.to_float("abc") == 0.0
        assert BasicConvertor.to_float([1, 2, 3]) == 0.0
        assert BasicConvertor.to_float((1, 2, 3)) == 0.0
        assert BasicConvertor.to_float({"a": 1, "b": 2}) == 0.0

        assert BasicConvertor.to_float("123", 100.0) == 123.0
        assert BasicConvertor.to_float("abc", 100.0) == 100.0
        with pytest.raises(ConversionError):
            BasicConvertor.to_float("sda", raise_exception=True)

    @classmethod
    def test_convert_to_bool(cls) -> None:
        assert BasicConvertor.to_bool("123")
        assert BasicConvertor.to_bool("123.456")
        assert BasicConvertor.to_bool(True)
        assert not BasicConvertor.to_bool(False)
        assert BasicConvertor.to_bool("真")
        assert BasicConvertor.to_bool("√")
