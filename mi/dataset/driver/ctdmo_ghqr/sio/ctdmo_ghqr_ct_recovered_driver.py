#!/usr/bin/env python

"""
@package mi.dataset.driver.ctdmo_ghqr.sio.ctdmo_ghqr_sio_ct_recovered
@file mi-dataset/mi/dataset/driver/ctdmo_ghqr/sio/ctdmo_ghqr_sio_ct_recovered_driver.py
@author Emily Hahn
@brief Driver for the ctdmo_ghqr_sio instrument ct recovered data
"""
import os
import re

from mi.core.log import get_logger
from mi.core.exceptions import DatasetParserException

from mi.dataset.dataset_parser import DataSetDriverConfigKeys
from mi.dataset.dataset_driver import DataSetDriver
from mi.dataset.parser.ctdmo_ghqr_ct_sio import CtdmoGhqrRecoveredCtParser, PARSED_SERIAL_ID_KEY

FILENAME_REGEX = r'SBE37-IM_(\d+)_\d{4}_\d{2}_\d{2}.hex'
FILENAME_MATCHER = re.compile(FILENAME_REGEX)


def parse(basePythonCodePath, sourceFilePath, particleDataHdlrObj):
    """
    This is the method called by Uframe
    :param basePythonCodePath This is the file system location of mi-dataset
    :param sourceFilePath This is the full path and filename of the file to be parsed
    :param particleDataHdlrObj Java Object to consume the output of the parser
    :return particleDataHdlrObj
    """

    log = get_logger()

    with open(sourceFilePath, 'r') as stream_handle:

        def exception_callback(exception):
                log.debug("Exception: %s", exception)
                particleDataHdlrObj.setParticleDataCaptureFailure()

        # extract the serial number from the file name
        serial_num = get_serial_num_from_filepath(sourceFilePath)

        parser_config = {
            DataSetDriverConfigKeys.PARTICLE_MODULE: 'mi.dataset.parser.ctdmo_ghqr_sio',
            DataSetDriverConfigKeys.PARTICLE_CLASS: ['CtdmoGhqrRecoveredInstrumentDataParticle'],
            PARSED_SERIAL_ID_KEY: serial_num
        }

        parser = CtdmoGhqrRecoveredCtParser(parser_config, stream_handle, exception_callback)

        # create and instance of the concrete driver class defined below
        driver = DataSetDriver(parser, particleDataHdlrObj)
        driver.processFileStream()

    return particleDataHdlrObj


def get_serial_num_from_filepath(filepath):
    """
    Parse the serial number from the file path
    :param filepath: The full path of the file to extract the serial number from the name
    :return: serial number
    """

    # get just the filename from the full path
    filename = os.path.basename(filepath)

    # match the filename, serial number is the first group
    filename_match = FILENAME_MATCHER.match(filename)

    # can't run parser without the serial number, raise an exception if it can't be found
    if not filename_match:
        raise DatasetParserException("Unable to parse serial number from file name %s", filename)

    # return serial number as an int
    return int(filename_match.group(1))
