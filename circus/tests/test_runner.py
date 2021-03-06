from tornado.testing import gen_test
from circus.tests.support import TestCircus, poll_for


def Dummy(test_file):
    with open(test_file, 'w') as f:
        f.write('..........')
    return 1


class TestRunner(TestCircus):

    @gen_test
    def test_dummy(self):
        yield self.start_arbiter('circus.tests.test_runner.Dummy')
        self.assertTrue(poll_for(self.test_file, '..........'))
        yield self.stop_arbiter()
