#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2019 Red Hat, Inc.
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
import hmac
from datetime import datetime, timedelta

from dciauth.v2.headers import generate_headers, TIMESTAMP_FORMAT


def is_valid(request, credential, headers):
    lowered_headers = _lower(headers)
    if "authorization" not in lowered_headers:
        return False
    parsed_headers = _parse_headers(lowered_headers)
    claimed_request = _get_claimed_request(request, parsed_headers)
    claimed_credential = _get_claimed_credential(credential, parsed_headers)
    claimed_headers = _lower(generate_headers(claimed_request, claimed_credential))
    return _signature_equals(lowered_headers, claimed_headers)


def is_expired(headers, now=None):
    timestamp = _parse_timestamp(_lower(headers))
    if timestamp:
        timestamp = datetime.strptime(timestamp, TIMESTAMP_FORMAT)
        now = now or datetime.utcnow()
        one_day = timedelta(hours=24)
        return abs(now - timestamp) > one_day
    return True


def _find_in_str_between(string, first, last):
    try:
        start = string.index(first) + len(first)
        end = string.index(last, start)
        return string[start:end]
    except ValueError:
        return ""


def _lower(headers):
    return {key.lower(): value for key, value in headers.items()}


def _parse_timestamp(headers):
    aws_date_header = "x-amz-date"
    dci_date_header = "x-dci-date"
    if aws_date_header not in headers and dci_date_header not in headers:
        return None
    return (
        headers[aws_date_header]
        if aws_date_header in headers
        else headers[dci_date_header]
    )


def _parse_headers(headers):
    authorization = headers.get("authorization")
    algorithm, credential, signed_headers, _ = authorization.split(" ")
    credential = _find_in_str_between(credential, "Credential=", ",").split("/")
    signed_headers = _find_in_str_between(signed_headers, "SignedHeaders=", ",")
    timestamp = _parse_timestamp(headers)
    return {
        "host": headers.get("host"),
        "algorithm": algorithm,
        "client_type": credential[0],
        "client_id": credential[1],
        "datestamp": credential[2],
        "region": credential[3],
        "service": credential[4],
        "request_type": credential[5],
        "signed_headers": signed_headers,
        "canonical_headers": {h: headers[h] for h in signed_headers.split(";")},
        "timestamp": timestamp,
        "content-type": headers.get("content-type", "application/json"),
    }


def _get_claimed_request(request, headers):
    claimed_request = headers
    claimed_request.update(
        {
            "method": request.get("method", "GET"),
            "endpoint": request.get("endpoint", "/"),
            "params": request.get("params", {}),
            "payload": request.get("payload", {}),
        }
    )
    return claimed_request


def _get_claimed_credential(credential, headers):
    return {
        "access_key": "%s/%s" % (headers["client_type"], headers["client_id"]),
        "secret_key": credential["secret_key"],
    }


def _get_signature(headers):
    kv_signature = headers.get("authorization").split(" ")[3]
    signature = kv_signature.split("Signature=")[1]
    return signature.encode("utf-8")


def _signature_equals(headers, generated_headers):
    signature1 = _get_signature(headers)
    signature2 = _get_signature(generated_headers)
    return hmac.compare_digest(signature1, signature2)
