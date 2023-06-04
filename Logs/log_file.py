import inspect
import logging


class log_class:
    def test_log(self):
        loggerName = inspect.stack()[1][3]
        logger = logging.getLogger(loggerName)
        '''it will tell that right now this particular test file is being run 
        and the logs are printed in regarding to that test file'''
        filename = logging.FileHandler('./Logs/logfile.log')
        # FileHandler method gives info. about the logging file where all the logs will be printed
        formatter = logging.Formatter("%(asctime)s : %(levelname)s : %(name)s : %(message)s")
        # Above the format is decided like in what format the log message is printed
        filename.setFormatter(formatter)
        # Above the format is appended to filehandler to pass the format info. to log file

        logger.addHandler(filename)

        logger.setLevel(
            logging.INFO)  # it will print all the messages from and below the info level and skip the debug messages
        # below is the order of the type of logs
        # logger.debug("This is a debug statement")
        # logger.info("This is information")
        # logger.warning("This is a warning")
        # logger.error("This is an error")
        # logger.critical("This is critical information")
        return logger
