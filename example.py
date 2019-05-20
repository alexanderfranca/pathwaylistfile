# -*- coding: utf-8 -*-

import pprint

from pathwaylistfile.pathwaylistfile import *

plf = PathwayListFile('./tests/fixtures/pathway.list')

data = plf.pathways_super_classes() 

pprint.pprint(data)
