import logging

class ExcludeAutoreloadFilter(logging.Filter):
    def filter(self, record):
        # Exclude messages containing autoreload-related patterns
        autoreload_patterns = ['autoreload', 'Watching for file changes with StatReloader']
        for pattern in autoreload_patterns:
            if pattern in record.msg:
                return False  # Exclude this log message
        return True  # Include other log messages
