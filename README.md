# kwdyy-logger

シンプルで柔軟なロギングユーティリティ。  
`rich` があれば色付きログ、なければANSIエスケープで見やすく出力。  
設定は `logging_config.toml` で外部管理。

## インストール

```bash
uv sync
```

## 開発環境構築
```bash
uv sync --extra dev
```

## 使用例
```Python
from kwdyy_logger.logger import Logger

logger = Logger()
logger.info("アプリ起動")
```
