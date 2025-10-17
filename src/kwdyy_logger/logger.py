from __future__ import annotations
import os
import tomllib  # Python 3.11+
from pathlib import Path
from datetime import datetime
import logging
from logging import Formatter, handlers, getLogger, Handler, StreamHandler
import inspect


LOG_FILE_NAME = f'app_{datetime.strftime(datetime.now(), "%Y%m%d")}.log'  # logファイルの名前


class Logger:
    """
    汎用ロギングクラス。

    richライブラリがあれば色付きログを、なければANSIエスケープで色を付けて出力。
    設定はTOMLファイルで外部管理可能。

    使用例:
        >>> logger = Logger()
        >>> logger.info("起動しました")

    注意:
        - ログファイルは日付ごとに作成されます。
        - 古いログは `remove_oldlog()` で削除できます。
    """
    
    def __init__(
            self,
            *,
            log_level: str = 'INFO',
            save_log_dir: str = 'logs'):
        self.log_dir: Path = Path(save_log_dir)
        self.log_backupcount: int = 3

        # --- 外部設定ファイルの読み込み ---
        config = self._load_logging_config()
        logging.config.dictConfig(config)

        caller_func_name: str = inspect.stack()[1].filename.split('/')[-1]  # 呼び出し元関数名
        self.logger = getLogger(name=caller_func_name)

    def debug(self, msg: str) -> None:
        self.logger.debug(msg, stacklevel=2)

    def info(self, msg: str) -> None:
        self.logger.info(msg, stacklevel=2)

    def warn(self, msg: str) -> None:
        self.logger.warning(msg, stacklevel=2)

    def error(self, msg: str, *, exc_info: bool = True) -> None:
        self.logger.error(msg, exc_info=exc_info, stacklevel=2)

    def critical(self, msg: str) -> None:
        self.logger.critical(msg, stacklevel=2)

    def remove_oldlog(self, *, max_num_log: int = 100) -> None:
        """ログディレクトリにmax_log_num以上logファイルがある場合、古いものから削除してmax_num_log個以下にする"""
        logs: list[Path] = list(self.log_dir.glob('*.log'))
        if len(logs) <= max_num_log:
            return  # 削除不要
    
        # ファイル名から日付を抽出してソート（古い順）
        log_name_pairs: list[tuple[Path, datetime]] = [
            (log, datetime.strptime(log.name[-12:-4], '%Y%m%d'))
            for log in logs
        ]
        log_name_pairs.sort(key=lambda x: x[1])  # 日付で昇順（古い順）
    
        # 削除すべきファイルの数
        num_to_remove = len(logs) - max_num_log
    
        for i in range(num_to_remove):
            remove_log_path: Path = log_name_pairs[i][0]
            remove_log_path.unlink()
            self.info(f'remove {remove_log_path.name}')
    
            # ローテーションされたlogファイル (logname_yyyymmdd.log.1) 等がある場合、それらも削除する
            for j in range(1, self.log_backupcount + 1):
                remove_rotating_log_path: Path = remove_log_path.with_suffix(f'.log.{j}')
                if remove_rotating_log_path.exists():
                    remove_rotating_log_path.unlink()
                    self.info(f'removed {remove_rotating_log_path.name}')

    def _create_log_gitignore(self) -> None:
        """logs/ ディレクトリに .gitignore を作成"""
        content: str = (
            '*\n'
            '!.gitignore\n'
        )
        gitignore_path = self.log_dir / '.gitignore'
        gitignore_path.write_text(content, encoding='utf-8')  # Path.write_text() で書き込み

    def _load_logging_config(self) -> dict:
        import logging.config

        # ログディレクトリを作成（中間ディレクトリも作成、既存なら無視）
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # .gitignore がなければ作成
        gitignore_path = self.log_dir / '.gitignore'
        if not gitignore_path.exists():
            self._create_log_gitignore()

        default_config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "rich_simple": {
                    "format": "%(message)s"  # RichHandlerに任せる
                },
                "detailed": {
                    "format": "%(asctime)s.%(msecs)03d %(levelname)7s %(message)s [%(name)s:%(lineno)d]",
                    "datefmt": "%Y/%m/%d %H:%M:%S"
                },
                "colored": {
                    "()": "kwdyy_logger.logger.ColoredFormatter"
                }
            },
            "handlers": {
                "file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "level": "DEBUG",
                    "formatter": "detailed",  # ファイルには詳細フォーマットを維持
                    "filename": str(self.log_dir / LOG_FILE_NAME),
                    "maxBytes": 16777216,
                    "backupCount": self.log_backupcount,
                    "encoding": "utf-8"
                }
            },
            "loggers": {
                "": {
                    "level": "DEBUG",
                    "handlers": ["console", "file"],
                    "propagate": False
                }
            }
        }

        config_path = Path("logging_config.toml")
        if config_path.exists():
            with open(config_path, "rb") as f:
                config = tomllib.load(f)

            # fileハンドラーがある場合のみ、filenameをコードで上書き
            if "handlers" in config and "file" in config["handlers"]:
                config["handlers"]["file"]["filename"] = str(self.log_dir / LOG_FILE_NAME)
        else:
            config = default_config

        try:
            from rich.logging import RichHandler
            console_handler = {
                "class": "rich.logging.RichHandler",
                "level": "INFO",
                "formatter": "rich_simple",  # ★ ここを変更
                "rich_tracebacks": True,
                "show_time": False,
                "show_level": True,
                "show_path": True,
                "markup": False,
                "highlighter": None
            }
        except ImportError:
            console_handler = {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "colored",
                "stream": "ext://sys.stdout"
            }

        config["handlers"]["console"] = console_handler
        return config

# --- ANSIエスケープを使った色付きフォーマッター ---
class ColoredFormatter(Formatter):
    COLORS = {
        'DEBUG': '\033[36m',   # シアン
        'INFO': '\033[32m',    # 緑
        'WARNING': '\033[33m', # 黄
        'ERROR': '\033[31m',   # 赤
        'CRITICAL': '\033[41m',# 白字赤背景
    }
    RESET = '\033[0m'

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.RESET)
        message = super().format(record)
        return f"{log_color}{message}{self.RESET}"

def main():
    """
    A simple demonstration of the Logger class.
    Initializes the logger using 'logging_config.toml' if it exists in the current directory,
    and logs messages at various levels.
    """
    print("Logger demo started.")
    print("This will use 'logging_config.toml' if present in the current directory.")
    
    try:
        # The Logger class will automatically look for 'logging_config.toml'
        logger = Logger()
        
        logger.info("Logger initialized for demo.")
        logger.debug("This is a debug message.")
        logger.info("This is an info message.")
        logger.warn("This is a warning message.")
        logger.error("This is an error message.", exc_info=False)
        logger.critical("This is a critical message.")
        
        print(f"Log messages have been written. Please check the configured log files (e.g., in the 'logs' directory).")

    except Exception as e:
        print(f"An unexpected error occurred during the logger demo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()