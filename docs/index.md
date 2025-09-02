<!-- Logger documentation master file, created by
     sphinx-quickstart on Mon Sep  1 18:49:23 2025.
     You can adapt this file completely to your liking, but it should at least
     contain the root `toctree` directive. -->

# Logger documentation
Logger は、柔軟で再利用可能なロギングユーティリティです。  
rich ライブラリがあれば色付きログを、なければ ANSI エスケープで見やすく出力します。  
設定は TOML ファイルで外部管理可能です。

## 機能
- コンソールとファイルへのログ出力
- 日次ログファイル（app_YYYYMMDD.log）
- rich による色付き・装飾付き出力
- 外部設定ファイル（logging_config.toml）対応
- 古いログの自動掃除

```{toctree}
:maxdepth: 2
:caption: Contents:
```

```{eval-rst}
.. automodule:: logger
   :members:
   :undoc-members:
   :show-inheritance:
```

## Indices and tables
- {ref}`genindex`
- {ref}`modindex`
- {ref}`search`