""" A (colored) logger for the application

Disclaimer: This file was not created by me, I found it online and adapted it for my own needs.
I would love to put the link for the original file here, but unfortunately I did not save it.

Utilisation:
from jobs.logger import getLogger

# create logger with default DEBUG lvl
logger = getLogger()

# create logger with customer log lvl
logger = getLogger("INFO")

# there are 5 logging levels, each with its own color
logger.debug("This is a debug message")             # usefull for sending information when debugging
                                                    # will be ignored if loggerlvl is INFO or higher
logger.info("This is an info message")              # use it to pass relevant information about the program execution
logger.warning("This is a warning message")         # use it to send important warnings. has background color - Yellow
logger.error("This is an error message")            # use it to send information about errors (that were handled) - RED
logger.critical("This is a critical message")       # (I) use it to send information about SUCCESS - Green

"""

from logging import StreamHandler, DEBUG, getLogger as realGetLogger, Formatter

from colorama import Fore, Back, init, Style
init()


class ColourStreamHandler(StreamHandler):

    """ A colorized output SteamHandler """

    # Some basic colour scheme defaults
    colours = {
        'DEBUG': Fore.CYAN,
        'INFO': Back.CYAN,
        'WARN': Fore.YELLOW,
        'WARNING': Back.YELLOW + Fore.BLACK,
        'ERROR': Back.RED + Fore.WHITE,
        'CRIT': Back.RED + Fore.WHITE,
        'CRITICAL': Back.GREEN + Fore.WHITE
    }

    def emit(self, record):
        try:
            message = self.format(record)
            line = self.colours[
                record.levelname] + '{: <5} | '.format(record.levelname) #+ Style.RESET_ALL
            line += message + Fore.WHITE + '::{filename} : {lineno}'.format(filename=record.filename, lineno=record.lineno)
            line += Style.RESET_ALL
            self.stream.write(line)
            self.stream.write(getattr(self, 'terminator', '\n'))
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


def getLogger(name=None, fmt='%(message)s', lvl="DEBUG"):
    """ Get and initialize a colourised logging instance if the system supports
    it as defined by the log.has_colour
    :param name: Name of the logger
    :type name: str
    :param fmt: Message format to use
    :type fmt: str
    :return: Logger instance
    :rtype: Logger
    """
    log = realGetLogger(name)
    # Only enable colour if support was loaded properly
    handler = ColourStreamHandler()
    handler.setLevel(DEBUG)
    handler.setFormatter(Formatter(fmt))
    log.addHandler(handler)
    log.setLevel(lvl)
    log.propagate = 0  # Don't bubble up to the root logger
    return log


def main():
    log = getLogger('test')
    log.info('asdf')
    log.debug('qwerqwe')
    print


if __name__ == "__main__":
    main()