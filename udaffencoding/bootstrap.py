from . import udaff

import sys, codecs
if sys.stdout.encoding != 'udaff':
    sys.stdout = codecs.getwriter('udaff')(sys.stdout.buffer, 'strict')
if sys.stderr.encoding != 'udaff':
    sys.stderr = codecs.getwriter('udaff')(sys.stderr.buffer, 'strict')
