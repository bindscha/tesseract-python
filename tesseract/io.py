import logging
import struct

from tesseract import canonical


def read_xsc_graph(path):
    with open(path,'rb') as file:
        try:
            for chunk in iter((lambda:file.read(8)), ''):
                source = struct.unpack('I', chunk[0:4])[0]
                target = struct.unpack('I', chunk[4:8])[0]
                yield (source, target)
        except:
            pass


class PatternOutput:
    def __init__(self, file=None, canonicalize=True, sort=False, log_patterns=False):
        self.file = file
        self.canonicalize = canonicalize
        self.sort = sort
        self.log_patterns = log_patterns
        self.log = logging.getLogger('OUTP')

    def found(self, e, G, tpe=None):
        if self.file is not None or self.log_patterns is not None:
            if self.canonicalize:
                e = canonical.canonicalize(e, G)
            elif self.sort:
                e = sorted(e)

            if self.file is not None:
                self.file.write('%s\n' % str(e))

            if self.log_patterns:
                self.log.info('Found %s: %s' % (tpe, str(e)))
