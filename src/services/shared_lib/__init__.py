from shared_lib.config import Config
from shared_lib.logger import JSONLogger

lib_logger: JSONLogger = JSONLogger(
    Config.service_name,
    Config.log_file_path,
    Config.log_max_bytes,
    Config.log_backup_count,
)
