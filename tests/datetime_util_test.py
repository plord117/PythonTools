#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   datetime_util_test.py
@Date       :   2024/08/27
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/08/27
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""
# here put the import lib

import random
from datetime import date, datetime

import allure  # type: ignore
import pytest
from faker import Faker
from loguru import logger

from .context_test import DatetimeUtil, Quarter, TimeUnit

BASIC_FAKE = Faker()
BASIC_CHINESE_FAKE = Faker("zh_CN")
BASIC_TW_FAKE = Faker("zh_TW")
BASIC_US_FAKE = Faker("en-US")


@allure.feature("日期工具类")
@allure.description("日期工具类, 支持对时间、日期的相关操作")
@allure.tag("datetime", "tag")
class TestDateTimeUtil:
    TEST_ROUND = 10

    @allure.story("时间获取")
    @allure.description("工具类支持获取当前时间、指定时间、随机时间等")
    class TestGetDt:
        @allure.title("测试获取随机datetime对象")
        def test_get_random_datetime(self):
            with allure.step("步骤1:测试随机时间，不带时区信息"):
                for _ in range(TestDateTimeUtil.TEST_ROUND):
                    res = DatetimeUtil.get_random_datetime()
                    logger.debug(f"{res=}")

            with allure.step("步骤2:测试随机时间，带时区信息"):
                for _ in range(TestDateTimeUtil.TEST_ROUND):
                    res = DatetimeUtil.get_random_datetime(random_tz=True)
                    logger.debug(f"{res=}")

        @allure.title("测试获取随机date对象")
        def test_get_random_date(self):
            with allure.step("步骤1:测试随机日期，不指定任何参数"):
                for _ in range(TestDateTimeUtil.TEST_ROUND):
                    dt = DatetimeUtil.get_random_date()
                    assert isinstance(dt, date)
                    logger.debug(dt)

            with allure.step("步骤2:测试随机日期，指定开始日期"):
                start = date(1998, 4, 24)
                for _ in range(TestDateTimeUtil.TEST_ROUND):
                    logger.debug(DatetimeUtil.get_random_date(start))

            with allure.step("步骤3:测试随机日期，指定开始日期和结束日期"):
                start = datetime(1998, 4, 24)
                end = datetime(2021, 4, 24)
                for _ in range(TestDateTimeUtil.TEST_ROUND):
                    logger.debug(DatetimeUtil.get_random_date(start, end))

            with allure.step("步骤4:测试随机日期，输入错误参数"):
                with pytest.raises(ValueError):
                    end = datetime(1998, 4, 24)
                    start = datetime(2021, 4, 24)
                    logger.debug(DatetimeUtil.get_random_date(start, end))

                with pytest.raises(ValueError):
                    start = datetime(1998, 4, 24)
                    end = datetime(1998, 4, 24)
                    logger.debug(DatetimeUtil.get_random_date(start, end))

        @allure.title("测试获取当前时间")
        def test_get_current(self):
            with allure.step("步骤1:测试获取当前年份"):
                logger.debug(DatetimeUtil.this_year())

            with allure.step("步骤2:测试获取当前季度"):
                logger.debug(DatetimeUtil.this_quarter())

            with allure.step("步骤3:测试获取当前月份"):
                logger.debug(DatetimeUtil.this_month)

            with allure.step("步骤4:测试获取当前日期"):
                logger.debug(DatetimeUtil.this_day())

            with allure.step("步骤5:测试获取当前小时"):
                logger.debug(DatetimeUtil.this_hour())

            with allure.step("步骤6:测试获取当前分钟"):
                logger.debug(DatetimeUtil.this_minute())

            with allure.step("步骤7:测试获取当前秒"):
                logger.debug(DatetimeUtil.this_second())

            with allure.step("步骤8:测试获取当前毫秒"):
                logger.debug(DatetimeUtil.this_millisecond())

            with allure.step("步骤9:测试获取当前timestamp"):
                logger.debug(DatetimeUtil.this_ts())

        @allure.title("测试获取本地时区")
        def test_get_local_tz(self) -> None:
            for _ in range(TestDateTimeUtil.TEST_ROUND):
                logger.debug(DatetimeUtil.get_local_tz())

        @allure.title("测试获取每月天数")
        def test_days_in_month(self) -> None:
            for i, v in enumerate([31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]):
                if i == 1:
                    continue
                assert DatetimeUtil.days_in_month(2024, i + 1) == v

            assert DatetimeUtil.days_in_month(2024, 2) == 29
            assert DatetimeUtil.days_in_month(2023, 2) == 28

        @allure.title("测试获取UTC时间")
        def test_get_utc_now(self) -> None:
            dt = DatetimeUtil.utc_now()
            logger.debug(f"{dt=}")

        @allure.title("测试获取年龄")
        def test_get_age(self) -> None:
            dt = datetime(1998, 4, 24)
            res_in_float_format = DatetimeUtil.get_age(dt, use_float_format=True)
            logger.debug(f"{res_in_float_format=}")
            res_in_int_format = DatetimeUtil.get_age(dt, use_float_format=False)
            logger.debug(f"{res_in_int_format=}")

            with pytest.raises(ValueError):
                DatetimeUtil.get_age(None)

    @allure.story("判断时间、日期属性")
    @allure.description("工具类支持判断时间、日期的属性，如是否闰年、是否同一天、是否同一月、是否同一年等")
    class TestDtProperty:
        @allure.title("测试是否闰年")
        def test_is_leap_year(self):
            assert DatetimeUtil.is_leap_year(2024)
            assert not DatetimeUtil.is_leap_year(2025)
            assert not DatetimeUtil.is_leap_year(1900)
            assert not DatetimeUtil.is_leap_year(2100)

        @allure.title("测试是否同一年")
        def test_is_same_year(self):
            for _ in range(TestDateTimeUtil.TEST_ROUND):
                d1 = DatetimeUtil.get_random_datetime()
                d2 = DatetimeUtil.get_random_datetime()

                assert DatetimeUtil.is_same_year(d1, d2) == (d1.year == d2.year)

            assert not DatetimeUtil.is_same_year(None, None)

        @allure.title("测试是否同一季度")
        def test_is_same_quarter(self):
            for _ in range(TestDateTimeUtil.TEST_ROUND):
                d1 = DatetimeUtil.get_random_datetime()
                d2 = DatetimeUtil.get_random_datetime()
                res = DatetimeUtil.is_same_quarter(d1, d2)
                logger.debug(f"d1={repr(d1)}, d2={repr(d2)}, {res=}")

        @allure.title("测试是否同一月")
        def test_is_same_month(self):
            for _ in range(TestDateTimeUtil.TEST_ROUND):
                d1 = DatetimeUtil.get_random_datetime()
                d2 = DatetimeUtil.get_random_datetime()

                assert DatetimeUtil.is_same_month(d1, d2) == (d1.year == d2.year and d1.month == d2.month)

            assert not DatetimeUtil.is_same_month(None, None)

        @allure.title("测试是否同一周")
        def test_is_same_week(self):
            for _ in range(TestDateTimeUtil.TEST_ROUND):
                d1 = DatetimeUtil.get_random_datetime(datetime(2024, 12, 1), datetime(2024, 12, 15))
                d2 = DatetimeUtil.get_random_datetime(datetime(2024, 12, 1), datetime(2024, 12, 15))
                res = DatetimeUtil.is_same_week(d1, d2)
                logger.debug(f"d1={repr(d1)}, d2={repr(d2)}, {res=}")

        @allure.title("测试是否同一天")
        def test_is_same_day(self):
            for _ in range(TestDateTimeUtil.TEST_ROUND):
                d1 = DatetimeUtil.get_random_datetime()
                d2 = DatetimeUtil.get_random_datetime()

                assert DatetimeUtil.is_same_day(d1, d2) == (
                    d1.year == d2.year and d1.month == d2.month and d1.day == d2.day
                )
                assert not DatetimeUtil.is_same_day(None, None)

        @allure.title("测试是否是工作日还是周末")
        def test_is_weekend_or_workday(self):
            with allure.step("步骤1:测试周末"):
                assert not DatetimeUtil.is_weekend(2024, 8, 26)
                assert not DatetimeUtil.is_weekend(2024, 8, 27)
                assert not DatetimeUtil.is_weekend(2024, 8, 28)
                assert not DatetimeUtil.is_weekend(2024, 8, 29)
                assert not DatetimeUtil.is_weekend(2024, 8, 30)
                assert DatetimeUtil.is_weekend(2024, 8, 10)
                assert DatetimeUtil.is_weekend(2024, 8, 11)

            with allure.step("步骤2:测试工作日"):
                assert DatetimeUtil.is_weekday(2024, 8, 26)
                assert DatetimeUtil.is_weekday(2024, 8, 27)
                assert DatetimeUtil.is_weekday(2024, 8, 28)
                assert DatetimeUtil.is_weekday(2024, 8, 29)
                assert DatetimeUtil.is_weekday(2024, 8, 30)
                assert not DatetimeUtil.is_weekday(2024, 8, 10)
                assert not DatetimeUtil.is_weekday(2024, 8, 11)

        @allure.title("测试datetime是否有时区信息")
        def test_has_tz(self):
            with allure.step("步骤1:测试有时区信息"):
                for _ in range(TestDateTimeUtil.TEST_ROUND):
                    dt = DatetimeUtil.get_random_datetime(random_tz=True)
                    assert DatetimeUtil.has_tz(dt)

            with allure.step("步骤2:测试无时区信息"):
                for _ in range(TestDateTimeUtil.TEST_ROUND):
                    dt = DatetimeUtil.get_random_datetime()
                    assert not DatetimeUtil.has_tz(dt)

    @allure.story("时间计算、转换")
    @allure.description("工具类支持对时间、日期进行计算、转换，如时间差、时间单位转换等")
    class TestDtCalc:
        @allure.title("测试时间差")
        def test_local_to_utc(self) -> None:
            with allure.step("步骤1:使用正确的输入"):
                for _ in range(TestDateTimeUtil.TEST_ROUND):
                    dt = DatetimeUtil.get_random_datetime()
                    dt = dt.astimezone(DatetimeUtil.get_random_tz())
                    utc_dt = DatetimeUtil.local_to_utc(dt)
                    logger.debug(f"{dt=}, {utc_dt=}")

            with allure.step("步骤2:使用错误的输入"):
                with pytest.raises(TypeError):
                    DatetimeUtil.local_to_utc(None)

        @allure.title("测试秒时间单位转换")
        def test_second_to_time(self):
            val = random.randrange(1000, 10000, 1000)
            res = DatetimeUtil.second_to_time(val)
            logger.debug(f"{val=}, {res=}")

        @allure.title("测试单位转换")
        def test_time_unit_convert(self):
            with allure.step("步骤1:测试正确的输入"):
                for i in range(TestDateTimeUtil.TEST_ROUND):
                    duration = i * 1000
                    res = DatetimeUtil.nanos_to_millis(duration)
                    res_second = DatetimeUtil.nanos_to_seconds(duration * 1000)
                    logger.debug(f"{i=}, {res=}, {res_second=}")

            with allure.step("步骤2:测试错误的输入"):
                with pytest.raises(ValueError):
                    DatetimeUtil.convert_time(None, TimeUnit.DAYS, TimeUnit.SECONDS)

                with pytest.raises(ValueError):
                    DatetimeUtil.convert_time(1000, None, TimeUnit.SECONDS)

                with pytest.raises(ValueError):
                    DatetimeUtil.convert_time(1000, TimeUnit.DAYS, None)

        @allure.title("测试 datetime 对象转换为ISO8601格式")
        def test_datetime_to_ISO8601(self):
            for _ in range(TestDateTimeUtil.TEST_ROUND):
                dt = DatetimeUtil.get_random_datetime()
                res = DatetimeUtil.datetime_to_ISO8601(dt)
                logger.debug(f"{dt=}, {res=}")

            with pytest.raises(TypeError):
                DatetimeUtil.datetime_to_ISO8601(None)

    @allure.story("其他功能")
    @allure.description("工具类提供其他功能，如获更精确的休眠等")
    class TestOther:
        @allure.title("测试更精确的sleep")
        def test_sleep(self) -> None:
            DatetimeUtil.sleep(1)

        @allure.title("测试获取当前时间戳")
        def test_nth_day_of_month(self) -> None:
            with allure.step("步骤1:测试获取当前月份的第1个星期几"):
                assert DatetimeUtil.nth_day_of_month(year=2024, month=8, weekday=1, n=1) == date(2024, 8, 5)
                assert DatetimeUtil.nth_day_of_month(year=2024, month=8, weekday=2, n=1) == date(2024, 8, 6)
                assert DatetimeUtil.nth_day_of_month(year=2024, month=8, weekday=3, n=1) == date(2024, 8, 7)
                assert DatetimeUtil.nth_day_of_month(year=2024, month=8, weekday=4, n=1) == date(2024, 8, 1)
                assert DatetimeUtil.nth_day_of_month(year=2024, month=8, weekday=5, n=1) == date(2024, 8, 2)
                assert DatetimeUtil.nth_day_of_month(year=2024, month=8, weekday=6, n=1) == date(2024, 8, 3)
                assert DatetimeUtil.nth_day_of_month(year=2024, month=8, weekday=7, n=1) == date(2024, 8, 4)

                assert DatetimeUtil.nth_day_of_month(year=2024, month=2, weekday=1, n=4) == date(2024, 2, 26)
                assert DatetimeUtil.nth_day_of_month(year=2024, month=2, weekday=2, n=4) == date(2024, 2, 27)
                assert DatetimeUtil.nth_day_of_month(year=2024, month=2, weekday=3, n=4) == date(2024, 2, 28)
                assert DatetimeUtil.nth_day_of_month(year=2024, month=2, weekday=4, n=4) == date(2024, 2, 22)
                assert DatetimeUtil.nth_day_of_month(year=2024, month=2, weekday=5, n=4) == date(2024, 2, 23)
                assert DatetimeUtil.nth_day_of_month(year=2024, month=2, weekday=6, n=4) == date(2024, 2, 24)
                assert DatetimeUtil.nth_day_of_month(year=2024, month=2, weekday=7, n=4) == date(2024, 2, 25)

            with allure.step("步骤2:测试获取不存在的日期"):
                with pytest.raises(IndexError):
                    DatetimeUtil.nth_day_of_month(year=2024, month=2, weekday=1, n=15)

                with pytest.raises(IndexError):
                    DatetimeUtil.nth_day_of_month(year=2024, month=2, weekday=9, n=1)

                with pytest.raises(IndexError):
                    DatetimeUtil.nth_day_of_month(year=2024, month=332, weekday=1, n=1)

                with pytest.raises(IndexError):
                    DatetimeUtil.nth_day_of_month(year=2024, month=2, weekday=5, n=5)

    @allure.story("时间偏移功能")
    @allure.description("工具类提供时间偏移功能，如获取指定时间的前后几天、月、年等")
    class TestOffset:
        @allure.title("测试获取指定时间的前后几天")
        def test_offset_day(self) -> None:
            with allure.step("步骤1:测试偏移年"):
                assert DatetimeUtil.offset_year(datetime(2024, 1, 1), 1) == datetime(2025, 1, 1)
                assert DatetimeUtil.offset_year(datetime(2024, 1, 1), -1) == datetime(2023, 1, 1)

            with allure.step("步骤2:测试偏移季度"):
                assert DatetimeUtil.offset_quarter(datetime(2024, 1, 1), 1) == Quarter.Q2
                assert DatetimeUtil.offset_quarter(datetime(2024, 1, 1), -1) == Quarter.Q4
                assert DatetimeUtil.offset_quarter(datetime(2024, 1, 1), 2) == Quarter.Q3

            with allure.step("步骤3:测试偏移月"):
                assert DatetimeUtil.offset_month(datetime(2024, 1, 1), 1) == datetime(2024, 2, 1)
                assert DatetimeUtil.offset_month(datetime(2024, 1, 1), -1) == datetime(2023, 12, 1)
                assert DatetimeUtil.offset_month(datetime(2024, 12, 31), 1) == datetime(2025, 1, 31)
                assert DatetimeUtil.offset_month(datetime(2024, 1, 31), 1) == datetime(2024, 2, 29)

            with allure.step("步骤4:测试偏移周"):
                assert DatetimeUtil.offset_week(datetime(2024, 12, 1), 1) == datetime(2024, 12, 8)
                assert DatetimeUtil.offset_week(datetime(2024, 12, 1), -1) == datetime(2024, 11, 24)
                assert DatetimeUtil.offset_week(datetime(2024, 12, 31), 1) == datetime(2025, 1, 7)
                assert DatetimeUtil.offset_week(datetime(2024, 12, 31), -1) == datetime(2024, 12, 24)

            with allure.step("步骤5:测试偏移日"):
                assert DatetimeUtil.offset_day(datetime(2024, 12, 1), 1) == datetime(2024, 12, 2)
                assert DatetimeUtil.offset_day(datetime(2024, 12, 1), -1) == datetime(2024, 11, 30)
                assert DatetimeUtil.offset_day(datetime(2024, 12, 31), 4) == datetime(2025, 1, 4)
                assert DatetimeUtil.offset_day(datetime(2024, 12, 31), -4) == datetime(2024, 12, 27)
                assert DatetimeUtil.offset_day(datetime(2024, 2, 29), 1) == datetime(2024, 3, 1)
                assert DatetimeUtil.offset_day(datetime(2024, 1, 1), -5) == datetime(2023, 12, 27)

            with allure.step("步骤6:测试偏移小时"):
                assert DatetimeUtil.offset_hour(datetime(2024, 12, 1, 12), 1) == datetime(2024, 12, 1, 13)
                assert DatetimeUtil.offset_hour(datetime(2024, 12, 1, 12), -1) == datetime(2024, 12, 1, 11)
                assert DatetimeUtil.offset_hour(datetime(2024, 12, 1, 23), 1) == datetime(2024, 12, 2, 0)
                assert DatetimeUtil.offset_hour(datetime(2024, 12, 1, 0), -1) == datetime(2024, 11, 30, 23)

            with allure.step("步骤7:测试偏移分钟"):
                assert DatetimeUtil.offset_minute(datetime(2024, 12, 1, 12, 30), 1) == datetime(2024, 12, 1, 12, 31)
                assert DatetimeUtil.offset_minute(datetime(2024, 12, 1, 12, 30), -1) == datetime(2024, 12, 1, 12, 29)
                assert DatetimeUtil.offset_minute(datetime(2024, 12, 1, 12, 59), 1) == datetime(2024, 12, 1, 13, 0)
                assert DatetimeUtil.offset_minute(datetime(2024, 12, 1, 12, 0), -1) == datetime(2024, 12, 1, 11, 59)

            with allure.step("步骤8:测试偏移秒"):
                assert DatetimeUtil.offset_second(datetime(2024, 12, 1, 12, 30, 30), 1) == datetime(
                    2024, 12, 1, 12, 30, 31
                )
                assert DatetimeUtil.offset_second(datetime(2024, 12, 1, 12, 30, 30), -1) == datetime(
                    2024, 12, 1, 12, 30, 29
                )
                assert DatetimeUtil.offset_second(datetime(2024, 12, 1, 12, 30, 59), 1) == datetime(
                    2024, 12, 1, 12, 31, 0
                )

            with allure.step("步骤9:测试偏移毫秒"):
                assert DatetimeUtil.offset_millisecond(datetime(2024, 12, 1, 12, 30, 30, 100), 1) == datetime(
                    2024, 12, 1, 12, 30, 30, 1100
                )
                assert DatetimeUtil.offset_millisecond(datetime(2024, 12, 1, 12, 30, 30, 1100), -1) == datetime(
                    2024, 12, 1, 12, 30, 30, 100
                )

            with allure.step("步骤10:测试偏移微秒"):
                assert DatetimeUtil.offset_microsecond(datetime(2024, 12, 1, 12, 30, 30, 100), 1) == datetime(
                    2024, 12, 1, 12, 30, 30, 101
                )
                assert DatetimeUtil.offset_microsecond(datetime(2024, 12, 1, 12, 30, 30, 100), -1) == datetime(
                    2024, 12, 1, 12, 30, 30, 99
                )

        @allure.title("测试快捷命令，获取相对于现在的偏移量")
        def test_offset_now(self) -> None:
            next_year = DatetimeUtil.next_year()
            next_quarter = DatetimeUtil.next_quarter()
            next_month = DatetimeUtil.next_month()

            logger.debug(f"{next_year=}, {next_quarter=}, {next_month=}")
