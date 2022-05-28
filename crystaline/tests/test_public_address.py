import pytest
from crystaline.public_address import public_address_generator as pa
from ecpy.curves import Point, Curve

from crystaline.public_address.public_address_generator import *


@pytest.fixture
def public():
    return pa.PublicAddressGenerator(123456789)


def test_public_address(public):
    assert public.public_address == "15QeDZLy4gst8A6jDY6T6VjNWgPHMR6dZp5AvUg2CBbRMpgG"


def test_curve(public):
    assert public.curve == Curve.get_curve(CURVE_NAME)


def test_public_key(public):
    assert public.public_key == Point(
        0xBE31100E124D42A7E436B369A60058D1127959B57D5269DC8A43827051A614A4187FE96EC1085501B1F5E47236366EEA396CFC010A143CFE,
        0xF7E790C1D0C7054B07972466329CA2563CD8B3C210A272A7E81908E0CE72CD4B48F923CF2734A6C5E140596257E17F5A79964ED75F751D50,
        Curve.get_curve(CURVE_NAME),
    )


def test_private_key(public):
    assert public.private_key == 123456789
