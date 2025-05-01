from auth_service.config import Config
from shared_lib.logger import JSONLogger

ServiceLog = JSONLogger(
    service_name=Config.service_name,
    log_file_path=Config.log_file_path,
    log_max_bytes=Config.log_max_bytes,
    log_backup_count=Config.log_backup_count,
)
