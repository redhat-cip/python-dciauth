#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2017 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the 'License'); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import mock

from datetime import datetime

from dciauth.v2.headers import generate_headers


def test_empty_credential_returns_empty_header():
    request = {"endpoint": "/api/v1/identity"}
    credential = {}
    assert generate_headers(request, credential) == {}


@mock.patch("dciauth.v2.headers.get_now")
def test_credential_field_in_autorization_header(get_now):
    get_now.return_value = datetime(2017, 12, 15, 11, 19, 29)
    request = {
        "service": "api2",
        "region": "BHS4",
        "algorithm": "DCI3-HMAC-SHA256",
        "request_type": "dci3_request",
    }
    credential = {
        "access_key": "feeder/464cc0a3-d638-a69e-4081-4c80261f3ba5",
        "secret_key": "0nqAfEUJr3OWO8YnyjlGf2h2lrmz3MD343ECjyDTCr3lphcRND2cNESYuo5IXA8t",
    }
    authorization_header = generate_headers(request, credential)["Authorization"]
    assert "DCI3-HMAC-SHA256" in authorization_header
    assert (
        "Credential=feeder/464cc0a3-d638-a69e-4081-4c80261f3ba5/20171215/BHS4/api2/dci3_request"
        in authorization_header
    )


@mock.patch("dciauth.v2.headers.get_now")
def test_generate_headers_default_values(get_now):
    get_now.return_value = datetime(2017, 12, 15, 11, 19, 29)
    request = {
        "endpoint": "/api/v1/users",
        "params": {"limit": 100, "embed": "teams"},
    }
    credential = {
        "access_key": "remoteci/464cc0a3-d638-4081-a69e-4c80261f3ba5",
        "secret_key": "0nqAfEUJr3OWO8YnyjlGf2h2lrmz3MD343ECjyDTCr3lphcRND2cNESYuo5IXA8t",
    }
    assert generate_headers(request, credential) == {
        "X-DCI-Date": "20171215T111929Z",
        "Authorization": "DCI2-HMAC-SHA256 Credential=remoteci/464cc0a3-d638-4081-a69e-4c80261f3ba5/20171215/BHS3/api/dci2_request, SignedHeaders=host;x-dci-date, Signature=aed55a70e89f8b541c9012afb2498b7139e64419f103efbea7a1b99744bd54ce",
    }


@mock.patch("dciauth.v2.headers.get_now")
def test_generate_headers_post(get_now):
    get_now.return_value = datetime(2017, 12, 15, 11, 19, 29)
    request = {
        "method": "POST",
        "endpoint": "/api/v1/users",
        "data": '{"name": "foo"}',
    }
    credential = {
        "access_key": "remoteci/464cc0a3-d638-4081-a69e-4c80261f3ba5",
        "secret_key": "0nqAfEUJr3OWO8YnyjlGf2h2lrmz3MD343ECjyDTCr3lphcRND2cNESYuo5IXA8t",
    }
    assert generate_headers(request, credential) == {
        "X-DCI-Date": "20171215T111929Z",
        "Authorization": "DCI2-HMAC-SHA256 Credential=remoteci/464cc0a3-d638-4081-a69e-4c80261f3ba5/20171215/BHS3/api/dci2_request, SignedHeaders=host;x-dci-date, Signature=ee6a1adfd78e47852b3b9daa1254849f0f4cce082de79de0957e53398c7946f8",
    }


@mock.patch("dciauth.v2.headers.get_now")
def test_generate_headers_post_with_payload(get_now):
    get_now.return_value = datetime(2017, 12, 15, 11, 19, 29)
    request = {
        "method": "POST",
        "endpoint": "/api/v1/users",
        "payload": {"name": "foo"},
    }
    credential = {
        "access_key": "remoteci/464cc0a3-d638-4081-a69e-4c80261f3ba5",
        "secret_key": "0nqAfEUJr3OWO8YnyjlGf2h2lrmz3MD343ECjyDTCr3lphcRND2cNESYuo5IXA8t",
    }
    assert generate_headers(request, credential) == {
        "X-DCI-Date": "20171215T111929Z",
        "Authorization": "DCI2-HMAC-SHA256 Credential=remoteci/464cc0a3-d638-4081-a69e-4c80261f3ba5/20171215/BHS3/api/dci2_request, SignedHeaders=host;x-dci-date, Signature=ee6a1adfd78e47852b3b9daa1254849f0f4cce082de79de0957e53398c7946f8",
    }


@mock.patch("dciauth.v2.headers.get_now")
def test_generate_headers_post_file(get_now):
    get_now.return_value = datetime(2017, 12, 15, 11, 19, 29)
    request = {
        "method": "POST",
        "endpoint": "/api/v1/jobs",
    }
    credential = {
        "access_key": "remoteci/464cc0a3-d638-4081-a69e-4c80261f3ba5",
        "secret_key": "0nqAfEUJr3OWO8YnyjlGf2h2lrmz3MD343ECjyDTCr3lphcRND2cNESYuo5IXA8t",
    }
    assert generate_headers(request, credential) == {
        "X-DCI-Date": "20171215T111929Z",
        "Authorization": "DCI2-HMAC-SHA256 Credential=remoteci/464cc0a3-d638-4081-a69e-4c80261f3ba5/20171215/BHS3/api/dci2_request, SignedHeaders=host;x-dci-date, Signature=8d0499f9179fd8efefa49628fc2d7a226224c4cb76495a5f9abf5cb4680f61c9",
    }


@mock.patch("dciauth.v2.headers.get_now")
def test_generate_headers_put(get_now):
    get_now.return_value = datetime(2017, 12, 15, 11, 19, 29)
    request = {
        "method": "PUT",
        "endpoint": "/api/v1/users",
        "data": '{"name": "foo"}',
    }
    credential = {
        "access_key": "remoteci/464cc0a3-d638-4081-a69e-4c80261f3ba5",
        "secret_key": "0nqAfEUJr3OWO8YnyjlGf2h2lrmz3MD343ECjyDTCr3lphcRND2cNESYuo5IXA8t",
    }
    assert generate_headers(request, credential) == {
        "X-DCI-Date": "20171215T111929Z",
        "Authorization": "DCI2-HMAC-SHA256 Credential=remoteci/464cc0a3-d638-4081-a69e-4c80261f3ba5/20171215/BHS3/api/dci2_request, SignedHeaders=host;x-dci-date, Signature=6e381497fd432306daa7ff33ba115006ae54b75a9dafc6bc58c8e58589d81b59",
    }


@mock.patch("dciauth.v2.headers.get_now")
def test_generate_headers_delete(get_now):
    get_now.return_value = datetime(2017, 12, 15, 11, 19, 29)
    request = {
        "method": "DELETE",
        "endpoint": "/api/v1/users/ef837f60-87f4-4432-a249-b4977ec5bb45",
    }
    credential = {
        "access_key": "remoteci/464cc0a3-d638-4081-a69e-4c80261f3ba5",
        "secret_key": "0nqAfEUJr3OWO8YnyjlGf2h2lrmz3MD343ECjyDTCr3lphcRND2cNESYuo5IXA8t",
    }
    assert generate_headers(request, credential) == {
        "X-DCI-Date": "20171215T111929Z",
        "Authorization": "DCI2-HMAC-SHA256 Credential=remoteci/464cc0a3-d638-4081-a69e-4c80261f3ba5/20171215/BHS3/api/dci2_request, SignedHeaders=host;x-dci-date, Signature=260e496d5d8bd13253831e1a41abfa0eea477707f1beefb9b92d59238670d62e",
    }


def test_generate_headers_with_claimed_stamps():
    request = {
        "method": "POST",
        "endpoint": "/api/v1/users",
        "data": '{"name": "foo"}',
        "timestamp": "20171215T111929Z",
        "datestamp": "20171215",
    }
    credential = {
        "access_key": "remoteci/464cc0a3-d638-4081-a69e-4c80261f3ba5",
        "secret_key": "0nqAfEUJr3OWO8YnyjlGf2h2lrmz3MD343ECjyDTCr3lphcRND2cNESYuo5IXA8t",
    }
    assert generate_headers(request, credential) == {
        "X-DCI-Date": "20171215T111929Z",
        "Authorization": "DCI2-HMAC-SHA256 Credential=remoteci/464cc0a3-d638-4081-a69e-4c80261f3ba5/20171215/BHS3/api/dci2_request, SignedHeaders=host;x-dci-date, Signature=ee6a1adfd78e47852b3b9daa1254849f0f4cce082de79de0957e53398c7946f8",
    }


@mock.patch("dciauth.v2.time.datetime.datetime")
def test_nrt_utcnow_should_be_called_one_time_in_order_to_generate_the_appropriate_signature(
    mocked_datetime,
):
    mocked_datetime.utcnow = mock.MagicMock(
        return_value=datetime(2020, 2, 8, 16, 12, 29)
    )
    request = {"method": "GET", "endpoint": "/api/v1/users"}
    credential = {
        "access_key": "remoteci/464cc0a3-d638-4081-a69e-4c80261f3ba5",
        "secret_key": "0nqAfEUJr3OWO8YnyjlGf2h2lrmz3MD343ECjyDTCr3lphcRND2cNESYuo5IXA8t",
    }
    generate_headers(request, credential)

    assert mocked_datetime.utcnow.call_count == 1
