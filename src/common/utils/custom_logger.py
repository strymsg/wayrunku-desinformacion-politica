"""
This is part of wayrunku-processing
Copyright Rodrigo Garcia 2023
"""

import logging
import os
import pathlib


class CustomLogger(logging.Logger):
    """Class to manage a custom logger

    Parameters
    ----------
    logging : obj
        logging object
    """
    handlers = []

    def __init__(self, name, logfile="data_app.log", minloglevel="DEBUG"):
        """Initialize logger

        Parameters
        ----------
        name : context
            context where logger runs
        """
        logging.Logger.__init__(self, name)
        self.configure(logfile, minloglevel)


    def close(self):
        """Method to close and flush all the handlers
        """
        for handler in self.handlers:
            handler.flush()
            handler.close()


    def configure(self, logfile, minloglevel):
        """Method to configure handlers, set level and set formatters.
        
        logfile: name of the logfile inside `LOG_PATH' defined path
        minloglevel: Default minmum loglevel, either; DEBUG, WARNING, INFO, ERROR, CRITICAL
        """
        console_handler = logging.StreamHandler()
        
        file_handler = logging.FileHandler(
            #filename=str(log_path.joinpath(logfile).absolute()),
            filename='logs/logs.log',
            mode='a'
        )

        log_level=logging.DEBUG
        if minloglevel == "INFO":
            log_level = logging.INFO
        elif minloglevel == "DEBUG":
            log_level = logging.DEBUG
        elif minloglevel == "WARNING":
            log_level = logging.WARN
        elif minloglevel == "ERROR":
            log_level = logging.ERROR
        elif minloglevel == "CRITICAL":
            log_level = logging.CRITICAL
            
        #console_handler.setLevel(logging.ERROR)
        console_handler.setLevel(logging.DEBUG)
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s (%(name)s) -[%(levelname)s] - %(message)s",
            datefmt="%d-%b-%y %H:%M:%S"
            )
        logging.setLevel = log_level
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        self.handlers = self.handlers + [console_handler, file_handler]

