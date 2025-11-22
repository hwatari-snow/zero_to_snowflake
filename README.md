# Getting Started from Zero to Snowflake

## 概要

> 本レポジトリは [Zero to Snowflake](https://quickstarts.snowflake.com/guide/zero_to_snowflake) を原本とする、日本語化済みサンプルファイルをまとめたものです。

このガイドでは、全5章に分けてSnowflakeのコア機能について触れていきます。

### 1. Getting Started with Snowflake
まずはスケーラブルな計算のための仮想ウェアハウス、シームレスなデータ復旧のためのUNDROP、コスト制御のためのリソースモニターなどの基本機能を確認します。

### 2. Simple Data Pipeline
外部データおよび半構造化データを取り込み、Dynamic Tables (動的テーブル) を使用して宣言的に変換することにより、自動化されたデータパイプラインの構築方法を学びます。

### 3. Apps & Collaboration
最後に、Snowflake Marketplaceからデータを取得して分析を豊かにし、Streamlitを使用してデータ上に直接インタラクティブアプリケーションを構築する方法に触れることができます。


## 📂 フォルダ構造

```
zero_to_snowflake/
├── Scripts/              # SQLスクリプトファイル（元のスクリプト）
│   ├── setup.sql
│   ├── vignette-1.sql
│   ├── vignette-2.sql
│   ├── vignette-3.sql
│   ├── vignette-4-aisql(Appendix).sql
│   ├── vignette-4-copilot(Appendix).sql
│   └── vignette-5(appendix).sql
├── Notebook/            # Jupyter Notebook形式（Snowflake Notebook対応）
│   ├── setup.ipynb
│   ├── vignette-1.ipynb
│   ├── vignette-2.ipynb
│   ├── vignette-3.ipynb
│   ├── vignette-4-aisql.ipynb
│   ├── vignette-4-copilot.ipynb
│   ├── vignette-5-governance.ipynb
│   └── README.md
└── streamlit/           # Streamlitアプリケーション
    └── streamlit_app.py
```

## 🚀 使い方

### SQLスクリプトの実行

1. Snowflake WebUIにログイン
2. Worksheetを開く
3. `Scripts/`フォルダからSQLファイルをコピー＆ペースト
4. 順番に実行

### Notebookの使用

1. Snowflake WebUIの「Projects」→「Notebooks」に移動
2. 「Import .ipynb file」をクリック
3. `Notebook/`フォルダからファイルを選択してインポート
4. セルを順番に実行

詳細は[Notebook/README.md](./Notebook/README.md)を参照してください。

## ステップバイステップ ガイド

前提条件、環境設定、ステップバイステップガイド、および手順については、[クイックスタートガイド](https://quickstarts.snowflake.com/guide/zero_to_snowflake)をご参照ください。

## 🔗 参考リンク
- [Snowflake Documentation](https://docs.snowflake.com/)
- [Snowflake Notebooks](https://docs.snowflake.com/en/user-guide/ui-snowsight-notebooks)
- [Tasty Bytes Quickstart](https://quickstarts.snowflake.com/guide/tasty_bytes_introduction/)


## Appendix
### 4. Snowflake Cortex AI
データベース内インテリジェンスのためのCortex機能と、コード作成支援のためのCopilotを活用したSnowflakeのAIレイヤーを紹介します。

### 5. Governance with Horizon
ガバナンスは、ロールベースのアクセス制御、列レベルマスキング、行レベルポリシーを使用してデータを保護するSnowflake Horizonを通じて確立され、Trust Centerによりセキュリティ監視が可能になります。

--- 
**作成者**: Hiroki Watari  
**最終更新**: 2025/11/22
