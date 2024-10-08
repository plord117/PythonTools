#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   string_util_test.py
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

import allure  # type: ignore
import pytest
from faker import Faker
from loguru import logger

from .context_test import (
    StringUtil,
    StringValidator,
)

BASIC_FAKE = Faker()
BASIC_CHINESE_FAKE = Faker("zh_CN")
BASIC_TW_FAKE = Faker("zh_TW")
BASIC_US_FAKE = Faker("en-US")


@allure.feature("字符串工具类")
@allure.description("字符串工具类,用于字符串处理相关操作")
@allure.tag("util", "string")
class TestStringUtil:
    @allure.story("判断字符串的相关状态")
    @allure.description("测试判断字符串的相关状态,例如是否为空等")
    class TestStringState:
        @allure.title("测试判断字符串是否相等")
        def test_equals(self):
            with allure.step("步骤1:测试不忽略大小写"):
                s1 = "hello"
                s2 = "HELLO"
                assert not StringUtil.equals(s1, s2, case_insensitive=False)

                s1 = "hello"
                s2 = "hello"
                assert StringUtil.equals(s1, s2)

            with allure.step("步骤2:测试忽略大小写"):
                s1 = "hello"
                s2 = "HELLO"
                assert StringUtil.equals(s1, s2, case_insensitive=True)

            with allure.step("步骤3:测试严格模式和非严格模式"):
                s1 = "hello "
                s2 = "hello"
                assert StringUtil.equals(s1, s2, strict_mode=False)
                assert not StringUtil.equals(s1, s2, strict_mode=True)

        @allure.title("测试字符串是否包含指定字符")
        def test_equals_any(self):
            assert StringUtil.equals_any("hello", "hello world", "hello")
            assert not StringUtil.equals_any("hello", "hello world", "world")

        @allure.title("测试字符串不想等")
        def test_not_equals(self):
            assert StringUtil.not_equals("hello", "world")
            assert not StringUtil.not_equals("hello", "hello")

        @allure.title("测试字符串是否包含数字")
        def test_contains_digit(self):
            assert StringUtil.contain_digit("hello123world")
            assert not StringUtil.contain_digit("helloworld")

        @allure.title("测试字符串是否包含字母")
        @allure.title("测试字符串是否为空")
        def test_is_empty(self) -> None:
            with allure.step("步骤1:测试字符串是否为空"):
                assert StringUtil.is_blank(None)
                assert StringUtil.is_blank("")
                assert StringUtil.is_blank(" \t\n")

            with allure.step("步骤2:测试字符串是否为非空"):
                assert StringUtil.is_not_blank("abc")
                assert StringUtil.is_not_blank("1231")
                assert StringUtil.is_all_blank("")
                assert StringUtil.is_all_blank(" ")
                assert StringUtil.is_not_blank("你好")
                assert StringUtil.is_all_blank("", " ", "  ", "\t\n")
                assert not StringUtil.is_all_blank("", "s", "b")
                assert not StringUtil.is_all_blank("s", "b")

            with allure.step("步骤3:测试多个字符串是否全为空"):
                assert StringUtil.is_all_blank(None, "", " \t\n")
                assert StringUtil.is_all_blank("", "", "")
                assert not StringUtil.is_all_blank(None, "", "你好")

            with allure.step("步骤4:测试多个字符串中是否有空"):
                assert StringUtil.has_blank("")
                assert StringUtil.has_blank(" ")
                assert StringUtil.has_blank("", "s", "b")
                assert not StringUtil.has_blank("s", "b")

        @allure.title("测试字符串判断开头和结尾")
        def test_start_and_end_with(self) -> None:
            with allure.step("步骤1:测试字符串是否以指定字符开头"):
                assert StringUtil.is_starts_with("hello world", "h")
                assert StringUtil.is_starts_with("hello world", "he")
                assert StringUtil.is_starts_with("hello world", "hello")
                assert not StringUtil.is_starts_with("hello world", "world")
                assert not StringUtil.is_starts_with("hello world", "l")

            with allure.step("步骤2:测试字符串是否以指定字符结尾"):
                assert StringUtil.is_ends_with("hello world", "d")
                assert StringUtil.is_ends_with("hello world", "ld")
                assert StringUtil.is_ends_with("hello world", "world")
                assert not StringUtil.is_ends_with("hello world", "he")
                assert not StringUtil.is_ends_with("hello world", "o")

            with allure.step("步骤3:测试字符串是否以指定的多个字符中的一个开头"):
                assert StringUtil.is_starts_with_any("hello world", "h", "he", "hello")
                assert StringUtil.is_starts_with_any("hello world", "he", "hello")
                assert not StringUtil.is_starts_with_any("hello world", "l", "ld")

            with allure.step("步骤4:测试字符串是否以指定的多个字符中的一个结尾"):
                assert StringUtil.is_ends_with_any("hello world", "d", "ld", "world")
                assert StringUtil.is_ends_with_any("hello world", "ld", "world")
                assert not StringUtil.is_ends_with_any("hello world", "he", "o")

        @allure.title("测试字符串是否被指定前后缀包裹")
        def test_is_surround(self) -> None:
            assert StringUtil.is_surround("hello world", "hello", "world")
            assert not StringUtil.is_surround("hello world", "Hello", "world", case_insensitive=False)
            assert StringUtil.is_surround("hello world", "Hello", "world", case_insensitive=True)

        @allure.title("测试字符串所有字符都是空白")
        def test_is_all_whitespace(self) -> None:
            assert StringUtil.is_all_whitespace("")
            assert StringUtil.is_all_whitespace(" \t\n")
            assert not StringUtil.is_all_whitespace("hello")

        @allure.title("测试字符串是否是unicode字符串")
        def test_is_unicode_str(self) -> None:
            assert StringUtil.is_unicode_str("h")

        @allure.title("测试字符串是否是文件分隔符")
        def test_is_file_separator(self) -> None:
            assert StringUtil.is_file_separator("/")
            assert StringUtil.is_file_separator("\\")
            assert not StringUtil.is_file_separator(" ")
            with pytest.raises(ValueError):
                assert not StringUtil.is_file_separator("")

        @allure.story("获取字符串的属性和方法")
        @allure.description("测试获取字符串的属性和方法,例如长度,大小写等")
        class TestStringProperties:
            @allure.title("测试获取字符串公共前后缀")
            def test_prefix_and_suffix(self) -> None:
                with allure.step("步骤1:测试获取字符串公共前缀"):
                    test_str1 = "hello world"
                    test_str2 = "hello python"
                    assert StringUtil.get_common_prefix(test_str1, test_str2) == "hello "

                with allure.step("步骤2:测试获取字符串公共后缀"):
                    test_2_str1 = "programming"
                    test_2_str2 = "progress"
                    assert StringUtil.get_common_prefix(test_2_str1, test_2_str2) == "progr"

                with allure.step("步骤3:测试获取字符串公共前后缀为空"):
                    test_prefix_str1 = "hello world"
                    test_prefix_str2 = "world hello"
                    assert StringUtil.get_common_prefix(test_prefix_str1, test_prefix_str2) == ""

                    test_suffix_str1 = "hello world"
                    test_suffix_str2 = "world hello"
                    assert StringUtil.get_common_suffix(test_suffix_str1, test_suffix_str2) == ""

            @allure.title("测试获取字符串长度和宽度")
            def test_get_string_length(self) -> None:
                with allure.step("步骤1:测试获取长度"):
                    assert StringUtil.get_length("hello world") == 11
                    assert StringUtil.get_length("1234567890") == 10
                    assert StringUtil.get_length("你好啊") == 3
                    assert StringUtil.get_length("") == 0

                with allure.step("步骤2:测试获取宽度"):
                    assert StringUtil.get_width("你好啊") == 6
                    assert StringUtil.get_width("1234567890") == 10
                    assert StringUtil.get_width("") == 0
                    assert StringUtil.get_width(None) == 0  # type: ignore
                    assert StringUtil.get_width("\t") == 1
                    assert StringUtil.get_width("\r") == 1
                    assert StringUtil.get_width("\n") == 1

            @allure.title("测试获取注释后的字符串信息")
            def test_get_annotation_str(self) -> None:
                with allure.step("步骤1:测试获取注释后的字符串信息，使用默认注释符号"):
                    assert StringUtil.get_annotation_str("hello world") == "-- hello world"
                    assert StringUtil.get_annotation_str("你好啊") == "-- 你好啊"
                    assert StringUtil.get_annotation_str("") == "-- "

                with allure.step("步骤2:测试获取注释后的字符串信息，使用自定义注释符号"):
                    assert StringUtil.get_annotation_str("hello world", "#") == "# hello world"
                    assert StringUtil.get_annotation_str("你好啊", "*") == "* 你好啊"
                    assert StringUtil.get_annotation_str("", "#") == "# "

            @allure.title("测试获取字符串居中信息")
            def test_center_msg(self) -> None:
                a = StringUtil.get_center_msg("hello world", "=", 40)
                b = StringUtil.get_center_msg("hello world", "=", 1)

                assert a == "=== hello world ===="
                assert b == " hello world "

            @allure.title("测试获取字符串的元音字母")
            def test_get_vowels_from_str(self) -> None:
                assert StringUtil.get_vowels_from_str("hello world") == "eoo"
                assert StringUtil.get_vowels_from_str("你好啊") == ""
                assert StringUtil.get_vowels_from_str("aeiounknknknknkjhknjniaodnwaondwo") == "aeiouiaoaoo"

    @allure.story("获取字符")
    @allure.description("测试获取字符,例如获取随机中文、小写字符等")
    class TestGetString:
        @allure.title("测试获取箱体字符串")
        def test_generate_box_string_from_dict_with_chinese(self):
            with allure.step("步骤1:测试带中文字符串的箱体字符串"):
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

            with allure.step("步骤2:测试获取不带中文字符串的箱体字符串"):
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

        @allure.title("测试获取随机字符串")
        def test_get_random_str(self):
            with allure.step("步骤1:测试获取随机小写字符串"):
                n = random.randint(1, 10)
                s = StringUtil.get_random_str_lower(n)
                assert s.islower() and StringUtil.get_length(s) == n

            with allure.step("步骤2:测试获取随机大写字符串"):
                n = random.randint(1, 10)
                s = StringUtil.get_random_str_upper(n)
                assert s.isupper() and StringUtil.get_length(s) == n

            with allure.step("步骤3:测试获取随机capitalized字符串"):
                n = random.randint(1, 10)
                s = StringUtil.get_random_str_capitalized(n)
                assert s[0].isupper() and s[1:].islower() and StringUtil.get_length(s) == n

            with allure.step("步骤4:测试获取随机字符串"):
                n = random.randint(1, 10)
                s = StringUtil.get_random_strs(n)
                assert StringUtil.get_length(s) == n and StringUtil.is_string(s)

            with allure.step("步骤5:测试获取随机中文字符串"):
                n = random.randint(1, 10)
                s = StringUtil.get_random_chinese_generator(n)
                for i in s:
                    assert StringValidator.is_chinese(i)

        @allure.title("测试获取罗马字符")
        def test_get_roman_num(self):
            generator = StringUtil.get_roman_range(1, 6)
            next(generator) == "I"
            next(generator) == "II"
            next(generator) == "III"
            next(generator) == "IV"
            next(generator) == "V"

        @allure.title("测试获取圆括号数字")
        def test_get_parentheses(self) -> None:
            assert StringUtil.get_circled_number(1) == "①"
            assert StringUtil.get_circled_number(4) == "④"

    @allure.story("字符串操作")
    @allure.description("测试字符串操作,例如字符串截取、替换、分割等")
    class TestStringOperation:
        @allure.title("测试字符串按长度分组")
        def test_group_by_length(cls) -> None:
            input_string = "abcdefghij"
            result = StringUtil.group_by_length(input_string, 3)
            assert result == ["abc", "def", "ghi", "j"]

        @allure.title("测试字符串缩写")
        def test_abbreviate_string(cls) -> None:
            assert StringUtil.abbreviate("abcdefg", 6) == "abc..."
            assert StringUtil.abbreviate(None, 7) == ""  # type: ignore
            assert StringUtil.abbreviate("abcdefg", 8) == "abcdefg"
            assert StringUtil.abbreviate("abcdefg", 4) == "a..."

            with pytest.raises(ValueError):
                StringUtil.abbreviate("abcdefg", 0)

        @allure.title("测试获取字符串分隔符之前的字符")
        def test_sub_before(cls) -> None:
            s1 = "2024-08-01"
            assert StringUtil.sub_before(s1, "-", False) == "2024"
            assert StringUtil.sub_before(s1, "-", True) == "2024-08"
            assert StringUtil.sub_before(s1, "年", False) == "2024-08-01"
            assert StringUtil.sub_before(None, "", True) == ""
            assert StringUtil.sub_before("", "", True) == ""
            assert StringUtil.sub_before("hello world", "", True) == "hello world"

        @allure.title("测试获取字符串分隔符之后的字符")
        def test_sub_after(cls) -> None:
            s1 = "2024-08-01"
            assert StringUtil.sub_after(s1, "-", False) == "08-01"
            assert StringUtil.sub_after(s1, "-", True) == "01"
            assert StringUtil.sub_before(s1, "年", False) == "2024-08-01"
            assert StringUtil.sub_before(None, "", True) == ""
            assert StringUtil.sub_before("", "", True) == ""
            assert StringUtil.sub_before("hello world", "", True) == "hello world"

        @allure.title("测试字符串移除所有的空白字符")
        def test_remove_blank(self) -> None:
            original = " hello world \n hello"
            res = StringUtil.remove_blank(original)
            assert res == "helloworldhello"

        @allure.title("测试移除前缀、后缀")
        def test_remove_prefix_and_suffix(self) -> None:
            with allure.step("步骤1:测试移除前缀"):
                s1 = "hello world"
                assert StringUtil.remove_prefix(s1, "hello") == " world"
                assert StringUtil.remove_prefix(s1, "world") == "hello world"
                assert StringUtil.remove_prefix(s1, "hello world") == ""

            with allure.step("步骤2:测试移除后缀"):
                s2 = "hello world"
                assert StringUtil.remove_suffix(s2, "world") == "hello "
                assert StringUtil.remove_suffix(s2, "hello") == "hello world"
                assert StringUtil.remove_suffix(s2, "hello world") == ""

        @allure.title("测试移除指定字符串")
        def test_remove_all(self) -> None:
            assert StringUtil.remove_all("hello world", "l", "h") == "eo word"
            assert StringUtil.remove_all("hello world", "l", "h", "w") == "eo ord"
            assert StringUtil.remove_all("hello world", "l", "h", "w", "o", "d") == "e r"

        @allure.title("测试根据空字符串转字符串")
        def test_empty_to_default(self) -> None:
            with allure.step("步骤1:测试空字符串转默认值"):
                assert StringUtil.empty_to_default("", "default") == "default"
                assert StringUtil.empty_to_default(" ", "default") == " "
                assert StringUtil.empty_to_default("s", "default") == "s"
                assert StringUtil.empty_to_default(None, "default") == "default"  # type: ignore

            with allure.step("步骤2:测试空字符串转None"):
                assert StringUtil.empty_to_none("") is None
                assert StringUtil.empty_to_none(" ") is not None
                assert StringUtil.empty_to_none("s") is not None

        @allure.title("测试None转字符串")
        def test_none_to_default(self) -> None:
            with allure.step("步骤1:测试None转默认值"):
                assert StringUtil.none_to_default(None, "default") == "default"  # type: ignore
                assert StringUtil.none_to_default(None, "default") == "default"  # type: ignore
                assert StringUtil.none_to_default("s", "default") == "s"

            with allure.step("步骤2:测试None转空字符串"):
                assert StringUtil.none_to_empty(None) == ""  # type: ignore
                assert StringUtil.none_to_empty("s") == "s"

        @allure.title("测试保留特定类型字符串")
        def test_retain_type_str(self) -> None:
            with allure.step("步骤1:测试保留数字字符串"):
                assert StringUtil.only_numerics("1234567890") == "1234567890"
                assert StringUtil.only_numerics("1234567890hello") == "1234567890"
                assert StringUtil.only_numerics("hello1234sdadsa567sdasd890") == "1234567890"

            with allure.step("步骤2:测试保留ASCII字符串"):
                assert StringUtil.only_ascii("hello world") == "hello world"
                assert StringUtil.only_ascii("hello1234sdadsa567sdasd890") == "hello1234sdadsa567sdasd890"
                assert StringUtil.only_ascii("a你b好c啊d") == "abcd"

            with allure.step("步骤3:测试保留小写字符"):
                assert StringUtil.only_lowercase("hello world") == "helloworld"
                assert StringUtil.only_lowercase("HELLO WORLD") == ""
                assert StringUtil.only_lowercase("a你b好c啊d") == "abcd"

            with allure.step("步骤4:测试保留大写字符"):
                assert StringUtil.only_uppercase("HELLO WORLD") == "HELLOWORLD"
                assert StringUtil.only_uppercase("hello world") == ""

            with allure.step("步骤5:测试保留英文字符"):
                StringUtil.only_alphabetic("hello1234sdadsa567sdasd890") == "hellosdadsasdasd"
                StringUtil.only_alphabetic("a你b好c啊d123213213") == "abcd"

            with allure.step("步骤6:测试保留字母和数字"):
                StringUtil.only_alphanumeric("你好啊, hello world 123") == "hello world 123"
                StringUtil.only_alphanumeric("a你b好c啊d123213213") == "abcd123213213"

            with allure.step("步骤7:测试保留可打印字符"):
                StringUtil.only_printable("你好啊, hello world 123\t\n") == "你好啊, hello world 123"
                StringUtil.only_printable("a你b好c啊\rd123213213") == "abcd123213213"

        @allure.title("测试字符串填充")
        def test_fill_string(self) -> None:
            with allure.step("步骤1:测试填充左侧字符"):
                assert StringUtil.fill_after("hello", "*", 10) == "hello*****"
                assert StringUtil.fill_after("hello", "*", 5) == "hello"
                assert StringUtil.fill_after("", "*", 10) == "**********"

            with allure.step("步骤2:测试填充右侧字符"):
                assert StringUtil.fill_before("hello", "*", 10) == "*****hello"
                assert StringUtil.fill_before("hello", "*", 5) == "hello"
                assert StringUtil.fill_before("", "*", 10) == "**********"

        @allure.title("测试字符串替换")
        def test_replace_string(self) -> None:
            with allure.step("步骤1:测试替换字符串"):
                assert StringUtil.replace_char_at("hello world", 0, "universe") == "universeello world"
                assert StringUtil.replace_char_at("hello world", 5, "universe") == "hellouniverseworld"

            with allure.step("步骤2:测试替换范围"):
                s = StringUtil.replace_range("hello world", "你好", 0)
                assert s == "你好llo world"

    @allure.story("字符串编码")
    @allure.description("测试字符串编码,例如罗马数字编码等")
    class TestStringEncode:
        @allure.title("测试字符串解码")
        def test_roman_decode(self) -> None:
            assert StringUtil.roman_decode("VII") == 7
            assert StringUtil.roman_decode("MCMXCIV") == 1994

        @allure.title("测试字符串编码")
        def test_roman_encode(self) -> None:
            assert StringUtil.equals(StringUtil.roman_encode(7), "VII")
            assert StringUtil.equals(StringUtil.roman_encode(1994), "MCMXCIV")
            assert StringUtil.equals(StringUtil.roman_encode(2020), "MMXX")
            assert StringUtil.equals(StringUtil.roman_encode(37), "XXXVII")

        @allure.title("测试字符串编码")
        def test_chinese_encode(self) -> None:
            with allure.step("步骤1:测试英文urf-8编码"):
                assert StringUtil.to_bytes("hello world").decode("utf-8") == "hello world"

            with allure.step("步骤2:测试中文utf-8编码"):
                assert StringUtil.to_bytes("你好啊").decode("utf-8") == "你好啊"

            with allure.step("步骤3:测试英文gbk编码"):
                assert StringUtil.to_bytes("hello world", "gbk").decode("gbk") == "hello world"

            with allure.step("步骤4:测试中文gbk编码"):
                assert StringUtil.to_bytes("你好啊", "gbk").decode("gbk") == "你好啊"

        @allure.title("测试字符串重复")
        def test_repeat_by_length(self) -> None:
            with allure.step("步骤1:测试按长度重复字符串"):
                assert StringUtil.repeat_by_length("hello", 10) == "hellohello"
                assert StringUtil.repeat_by_length("hello", 5) == "hello"
                assert StringUtil.repeat_by_length("", 10) == ""
                assert StringUtil.repeat_by_length("hello", 7) == "hellohe"

            with allure.step("步骤2:测试按数量重复字符串"):
                assert StringUtil.repeat_by_count("hello", 2) == "hellohello"
                assert StringUtil.repeat_by_count("hello", 1) == "hello"
                assert StringUtil.repeat_by_count("", 10) == ""

    @allure.story("字符串格式化")
    @allure.description("测试字符串格式化,例如货币格式化等")
    class TestStringFormat:
        @allure.title("测试字符串按货币格式化")
        def test_format_in_currency(self) -> None:
            assert StringUtil.equals(StringUtil.format_in_currency("123456789"), "123,456,789")
            assert StringUtil.equals(StringUtil.format_in_currency("123456789.45"), "123,456,789.45")
            assert StringUtil.equals(StringUtil.format_in_currency("-123456789.45"), "-123,456,789.45")
            assert StringUtil.equals(StringUtil.format_in_currency("0"), "0")
            assert StringUtil.equals(StringUtil.format_in_currency("-123456789"), "-123,456,789")

        @allure.title("测试字符串对齐")
        def test_align_text(self) -> None:
            s = "hello world, 你好啊"
            assert StringUtil.align_text(s, align="left") == " hello world, 你好啊"
            assert StringUtil.align_text(s, align="center") == " hello world, 你好啊 "
            assert StringUtil.align_text(s, align="right") == "hello world, 你好啊 "
