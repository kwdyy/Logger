from logger import Logger


def divide_by_zero():
    """意図的にゼロ除算エラーを発生させる関数"""
    return 1 / 0


def main():
    # Loggerのインスタンスを作成
    # → logging_config.toml があればそれを読み込み、なければデフォルト設定
    logger = Logger(save_log_dir="logs")

    # 各レベルのログを出力
    logger.debug("これはデバッグログです")
    logger.info("アプリケーションが正常に起動しました")
    logger.warn("これは警告メッセージです")

    # --- スタックトレース付きのエラーログ ---
    try:
        result = divide_by_zero()
    except Exception as e:
        logger.error(f"計算エラーが発生しました: {e}", exc_info=True)
        # exc_info=True でスタックトレースを出力

    logger.critical("重大な障害が発生しました！")

    # 古いログの掃除（テスト用に意図的に呼ぶ）
    # 実際には定期的に呼ぶ、または起動時などに実行
    logger.remove_oldlog(max_num_log=5)  # 5つ以上あれば古いものを削除

    print("✅ ログ出力と掃除が完了しました。logs/ ディレクトリを確認してください。")


if __name__ == "__main__":
    main()