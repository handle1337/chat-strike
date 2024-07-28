import sys
import os
import unittest
import time
import conparser.conparser as cp

log_file_path = os.path.normpath('tests/log.txt')
print(log_file_path)

class FileLogHandler(cp.ConLogEventHandler):

    def on_any_event(self, event):
        super().on_any_event(event)

    def on_modified(self, event):
        print(self.logfile_path)
        super().on_modified(event)

        if not event.is_directory:

            with open(self.logfile_path, 'rb') as logfile:
    
                username, message = cp.parse_log(game=self.game, line=cp.rt_file_read(logfile))
                if cp.BLACKLISTED_USERNAME != username: 
                    cp.sim_key_presses(cp.openai_interact(username, message))



class TestLogParsing(unittest.TestCase):
    def test_parser(self):
        pass

    def test_file_read(self):
        pass

    def test_game_detect(self):
        pass


def file_handler_test():
    file_log_handler = FileLogHandler()
    file_log_handler.game = "cs2"
    file_log_handler.logfile_path = log_file_path

    logfile = open(log_file_path, 'r') # Im not completely sure why but unless we have stream the observer wont work on linux
    cp.observer.schedule(file_log_handler, log_file_path)
    cp.observer.start()
    for i in range(60):
        time.sleep(1)

if __name__ == '__main__':
    #unittest.main()

    file_handler_test()
