import os
from pathlib import Path
import logging
from kwdyy_logger.logger import Logger
import shutil
from datetime import datetime

def setup_test_dir():
    log_dir = Path("test_logs")
    log_dir.mkdir(exist_ok=True)
    return log_dir

def teardown_test_dir():
    log_dir = Path("test_logs")
    if log_dir.exists():
        try:
            shutil.rmtree(log_dir)
        except PermissionError as e:
            print(f"⚠️ 削除失敗: {e}")

def close_logger_handlers(logger):
    """Loggerのすべてのハンドラーを閉じて削除"""
    for handler in logger.logger.handlers[:]:  # コピーで安全にイテレート
        handler.close()
        logger.logger.removeHandler(handler)

def test_logger_creates_log_directory():
    """Logger生成時にlogs/ディレクトリが作成されるかテスト"""
    # 前準備
    teardown_test_dir()  # 確実に削除
    log_dir = setup_test_dir()

    # テスト対象
    logger = Logger(save_log_dir="test_logs")
    close_logger_handlers(logger)

    # 検証
    assert log_dir.exists()
    assert log_dir.is_dir()

def test_logger_creates_gitignore():
    """logs/ディレクトリに.gitignoreが作成されるかテスト"""
    # 前準備
    teardown_test_dir()
    log_dir = setup_test_dir()
    gitignore = log_dir / ".gitignore"

    # .gitignoreが存在しない状態にする
    if gitignore.exists():
        gitignore.unlink()

    # テスト対象（再度Loggerを生成）
    logger = Logger(save_log_dir="test_logs")
    close_logger_handlers(logger)

    # 検証
    assert gitignore.exists()
    content = gitignore.read_text(encoding="utf-8")
    assert "*\n" in content
    assert "!.gitignore\n" in content

def test_logger_outputs_to_file():
    """ログが出力ファイルに書き込まれるかテスト"""
    # 前準備
    teardown_test_dir()
    log_dir = setup_test_dir()

    # テスト対象
    logger = Logger(save_log_dir="test_logs")
    logger.info("テストメッセージ")
    close_logger_handlers(logger)

    # 検証
    today = datetime.now().strftime("%Y%m%d")
    log_file = log_dir / f"app_{today}.log"
    assert log_file.exists(), f"{log_file} が作成されていません"
    content = log_file.read_text(encoding="utf-8")
    assert "テストメッセージ" in content

def test_remove_oldlog_removes_oldest():
    """remove_oldlog() が古いログを max_num_log まで減らすかテスト"""
    # 前準備
    teardown_test_dir()
    log_dir = setup_test_dir()

    # テスト用に複数のログファイルを作成（日付順に古い→新しい）
    test_dates = [
        "20200101",  # 最も古い
        "20210101",
        "20220101",
        "20230101",
        "20240101",
        "20250101",  # 最も新しい
    ]
    for date in test_dates:
        (log_dir / f"app_{date}.log").write_text(f"log from {date}")

    # テスト対象：最大3つまでに制限
    logger = Logger(save_log_dir="test_logs")

    # ハンドラを閉じてから削除処理を実行（WinError 32 対策）
    close_logger_handlers(logger)
    logger.remove_oldlog(max_num_log=3)  # 最大3ファイルまで許可

    # 検証：古い方から削除され、最新の3つが残る
    remaining_files = sorted([f.name for f in log_dir.glob("app_*.log")])
    expected_files = [
        "app_20240101.log",
        "app_20250101.log",
        f"app_{datetime.now().strftime('%Y%m%d')}.log",  # 当日分
    ]
    assert remaining_files == expected_files, f"期待されるファイル: {expected_files}, 実際: {remaining_files}"
