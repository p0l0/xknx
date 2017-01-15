import unittest

from xknx.knxip import KNXIPFrame, KNXIPServiceType, ConnectRequestType, \
    HPAI, ConnectRequest


class Test_KNXIP_ConnectRequest(unittest.TestCase):
    # pylint: disable=too-many-public-methods,invalid-name

    def test_connect_request(self):

        raw = ((0x06, 0x10, 0x02, 0x05, 0x00, 0x1a, 0x08, 0x01,
                0xc0, 0xa8, 0x2a, 0x01, 0x84, 0x95, 0x08, 0x01,
                0xc0, 0xa8, 0x2a, 0x01, 0xcc, 0xa9, 0x04, 0x04,
                0x02, 0x00))

        knxipframe = KNXIPFrame()
        knxipframe.from_knx(raw)

        self.assertTrue(isinstance(knxipframe.body, ConnectRequest))
        self.assertEqual(
            knxipframe.body.request_type,
            ConnectRequestType.TUNNEL_CONNECTION)
        self.assertEqual(
            knxipframe.body.control_endpoint,
            HPAI(ip_addr='192.168.42.1', port=33941))
        self.assertEqual(
            knxipframe.body.data_endpoint,
            HPAI(ip_addr='192.168.42.1', port=52393))

        knxipframe2 = KNXIPFrame()
        knxipframe2.init(KNXIPServiceType.CONNECT_REQUEST)
        knxipframe2.body.request_type = ConnectRequestType.TUNNEL_CONNECTION
        knxipframe2.body.control_endpoint = HPAI(
            ip_addr='192.168.42.1', port=33941)
        knxipframe2.body.data_endpoint = HPAI(
            ip_addr='192.168.42.1', port=52393)
        knxipframe2.normalize()

        self.assertEqual(knxipframe2.to_knx(), list(raw))


SUITE = unittest.TestLoader().loadTestsFromTestCase(Test_KNXIP_ConnectRequest)
unittest.TextTestRunner(verbosity=2).run(SUITE)
