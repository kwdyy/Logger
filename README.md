# kwdyy-logger

シンプルで柔軟なロギングユーティリティ。  
`rich` があれば色付きログ、なければANSIエスケープで見やすく出力。  
設定は `logging_config.toml` で外部管理。

## インストール

```bash
pip install .
```

## 開発環境構築
```bash
pip install -e .[dev]
```

## 使用例
```Python
from logger import Logger

logger = Logger()
logger.info("アプリ起動")
```

詳細は [ドキュメント](docs/_build/html/index.html) を参照。
