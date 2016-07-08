from nose.tools import with_setup
from unittest import TestCase
import os
import numpy as np
import logging

logger = logging.getLogger(name=__name__)

from pyrpl import RedPitaya
from pyrpl.redpitaya_modules import *
from pyrpl.registers import *
from pyrpl.bijection import Bijection

from pyrpl.spectrum_analyzer import SpectrumAnalyzer

class TestClass(object):
    @classmethod
    def setUpAll(self):
        # these tests wont succeed without the hardware
        if os.environ['REDPITAYA_HOSTNAME'] == 'unavailable':
            self.r = None
        else:
            self.r = RedPitaya()

    def test_spec_an(self):
        if self.r is None:
            return
        sa = SpectrumAnalyzer(self.r)
        sa.input = "asg1"
        self.r.asg1.frequency = 1e6
        self.r.asg1.trigger_source = 'immediately'

        sa.setup(center=1e6, span=1e5)
        curve = sa.curve()
        #Assumes out1 is connected with adc1...
        assert(curve.argmax()==500.0), curve.argmax()
