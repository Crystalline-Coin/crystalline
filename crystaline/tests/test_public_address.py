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
    assert public.public_key == Point(0xbe31100e124d42a7e436b369a60058d1127959b57d5269dc8a43827051a614a4187fe96ec1085501b1f5e47236366eea396cfc010a143cfe,
                                      0xf7e790c1d0c7054b07972466329ca2563cd8b3c210a272a7e81908e0ce72cd4b48f923cf2734a6c5e140596257e17f5a79964ed75f751d50,
                                      Curve.get_curve(CURVE_NAME))


def test_private_key(public):
    assert public.private_key == 123456789
