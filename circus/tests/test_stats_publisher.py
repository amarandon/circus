import mock
import json

import zmq

import unittest2 as unittest
from circus.stats.publisher import StatsPublisher


class TestStatsPublisher(unittest.TestCase):

    def test_publish(self):
        publisher = StatsPublisher()
        publisher.socket = mock.MagicMock()
        stat = {'subtopic': 1, 'foo': 'bar'}
        publisher.publish('foobar', stat)
        publisher.socket.send_multipart.assert_called_with(
            ['stat.foobar.1', json.dumps(stat)])

    def test_publish_reraise_zmq_errors(self):
        publisher = StatsPublisher()
        publisher.socket = mock.MagicMock()
        publisher.socket.closed = False
        publisher.socket.send_multipart.side_effect = zmq.ZMQError()

        stat = {'subtopic': 1, 'foo': 'bar'}
        self.assertRaises(zmq.ZMQError, publisher.publish, 'foobar', stat)

    def test_publish_silent_zmq_errors_when_socket_closed(self):
        publisher = StatsPublisher()
        publisher.socket = mock.MagicMock()
        publisher.socket.closed = True
        publisher.socket.send_multipart.side_effect = zmq.ZMQError()

        stat = {'subtopic': 1, 'foo': 'bar'}
        publisher.publish('foobar', stat)
