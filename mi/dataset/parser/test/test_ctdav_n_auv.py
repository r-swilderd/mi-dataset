#!/usr/bin/env python

"""
@package mi.dataset.parser.test
@fid marine-integrations/mi/dataset/parser/test/test_ctdav_n_auv.py
@author Jeff Roy
@brief Test code for a ctdav_n_auv data parser

NOTE:  As this is the 4th parser built from AuvCommonParser
full negative testing is not done.  See dosta_ln_auv and adcpa_n_auv
for complete testing of AuvCommonParser

"""

from nose.plugins.attrib import attr
import os

from mi.core.log import get_logger
log = get_logger()

from mi.idk.config import Config
from mi.dataset.test.test_parser import ParserUnitTestCase
from mi.dataset.parser.ctdav_n_auv import CtdavNAuvParser

RESOURCE_PATH = os.path.join(Config().base_dir(), 'mi', 'dataset',
                             'driver', 'ctdav_n', 'auv', 'resource')


@attr('UNIT', group='mi')
class CtdavNAuvTestCase(ParserUnitTestCase):
    """
    adcpa_n_auv Parser unit test suite
    """

    def test_simple_telem(self):
        """
        Read test data and pull out data particles.
        Assert that the results are those we expected.
        Expect the first input record to be skipped due to invalid timestamp
        """

        stream_handle = open(os.path.join(RESOURCE_PATH, 'subset_reduced.csv'), 'rU')

        parser = CtdavNAuvParser(stream_handle,
                                 self.exception_callback,
                                 is_telemetered=True)

        particles = parser.get_records(21)

        self.assert_particles(particles, 'ctdav_n_auv_telem_21.yml', RESOURCE_PATH)

        self.assertEqual(self.exception_callback_value, [])

        stream_handle.close()

    def test_simple_recov(self):
        """
        Read test data and pull out data particles.
        Assert that the results are those we expected.
        Expect the first input record to be skipped due to invalid timestamp
        """

        stream_handle = open(os.path.join(RESOURCE_PATH, 'subset_reduced.csv'), 'rU')

        parser = CtdavNAuvParser(stream_handle,
                                 self.exception_callback,
                                 is_telemetered=False)

        particles = parser.get_records(21)

        self.assert_particles(particles, 'ctdav_n_auv_recov_21.yml', RESOURCE_PATH)

        self.assertEqual(self.exception_callback_value, [])

        stream_handle.close()

    def test_long_stream_telem(self):
        """
        Read test data and pull out data particles.
        Assert the expected number of particles is captured and there are no exceptions
        """

        stream_handle = open(os.path.join(RESOURCE_PATH, 'subset.csv'), 'rU')

        parser = CtdavNAuvParser(stream_handle,
                                 self.exception_callback,
                                 is_telemetered=True)

        particles = parser.get_records(10000)

        self.assertEqual(len(particles), 8398)

        self.assertEqual(self.exception_callback_value, [])

        stream_handle.close()

