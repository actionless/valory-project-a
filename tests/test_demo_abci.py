# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2021-2023 Valory AG
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""Test module for Project A."""

import json
from io import StringIO
from logging import WARNING, getLogger
from typing import Generator
from unittest import mock

import pytest
from aea.protocols.base import Message, Serializer

from packages.author.skills.demo_abci.behaviours import DemoBehaviour
from packages.author.skills.demo_abci.handlers import ABCIHandler
from packages.author.skills.demo_abci.payloads import DemoPayload


class DummyContextManager:
    def __enter__(self, *_args, **_kwargs) -> None:
        pass

    def __exit__(self, *_args, **_kwargs) -> None:
        pass


class TestContext:
    agent_address = "foobar"
    logger = getLogger("test")
    logger.setLevel(WARNING)

    class benchmark_tool:
        class measure:
            def __init__(self, *_args, **_kwargs) -> None:
                pass

            class local(DummyContextManager):
                pass

            class consensus(DummyContextManager):
                pass

    class state:
        class round_sequence:
            current_round_id = "demo_round"
            last_round_id = "demo_round"
            current_round_height = 123


class TestSerializer(Serializer):
    @staticmethod
    def encode(message: Message) -> bytes:
        return json.dumps(message._body).encode("utf-8")

    @staticmethod
    def decode(input_text: bytes) -> Message:
        return Message.from_json(json.loads(input_text.decode("utf-8")))


class TestMessage(Message):
    serializer = TestSerializer


def handler_test_common(message: str) -> str:
    message = TestMessage({
        "dialogue_reference": message,
    })
    out_file = StringIO()
    with mock.patch("sys.stdout", new=out_file):
        ABCIHandler(name="smth", skill_context=TestContext).handle(message)
    return out_file.getvalue()


def test_handler_triggered() -> None:
    test_output = handler_test_common("hello")
    print(f"{test_output=}")
    assert "Message(sender=None,to=None,dialogue_reference=hello)" in test_output


def test_handler_skipped() -> None:
    test_output = handler_test_common("spam")
    print(f"{test_output=}")
    assert "Message(" not in test_output


def test_behaviour() -> None:
    test_result = None

    def mock_transaction(_self: DemoBehaviour, payload: dict) -> Generator:
        nonlocal test_result
        test_result = payload
        yield

    def round_end(_self: DemoBehaviour) -> Generator:
        yield

    with (
        mock.patch(
            "packages.author.skills.demo_abci.behaviours.DemoBehaviour.send_a2a_transaction",
            mock_transaction,
        ),
        mock.patch(
            "packages.author.skills.demo_abci.behaviours.DemoBehaviour.wait_until_round_end",
            round_end,
        ),
    ):
        for _ in DemoBehaviour(name="smth", skill_context=TestContext).async_act():
            pass

    assert isinstance(test_result, DemoPayload)
    assert len(test_result.content.split(" ")) == 2  # 2 words


@pytest.mark.e2e
def test_dummy_integration() -> None:
    """Dummy test integration."""
    assert True
