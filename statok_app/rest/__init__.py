import logging

# Logger setup
api_logger = logging.getLogger("api_logger")

log_format = logging.Formatter("[%(asctime)s] %(message)s")

file_handler = logging.FileHandler("api_log.log")
file_handler.setFormatter(log_format)

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_format)

api_logger.addHandler(file_handler)
api_logger.addHandler(console_handler)
api_logger.setLevel(logging.DEBUG)