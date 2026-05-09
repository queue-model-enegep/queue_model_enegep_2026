import time

from utils.print_styles import big_line



# Context manager to register the runtime of a file operation.
class MarkRuntime:
    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.end = time.perf_counter()
        big_line()
        print(f'TOTAL RUNTIME: {self.end - self.start:.6g} seconds')
        big_line()

