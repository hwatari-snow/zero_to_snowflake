# Zero to Snowflake - Notebook版

このフォルダには、ScriptsフォルダのSQLスクリプトをNotebook形式に変換したものが含まれています。

## 📚 Notebookファイル一覧

| Notebook | 説明 | 元のスクリプト |
|----------|------|----------------|
| `setup.ipynb` | データベース、スキーマ、ウェアハウスの初期セットアップ | `Scripts/setup.sql` |
| `vignette-1.ipynb` | 仮想ウェアハウス、クエリキャッシュ、リソースモニター | `Scripts/vignette-1.sql` |
| `vignette-2.ipynb` | シンプルなデータパイプライン、動的テーブル | `Scripts/vignette-2.sql` |
| `vignette-3.ipynb` | アプリケーションとコラボレーション、Marketplace | `Scripts/vignette-3.sql` |
| `vignette-4-aisql.ipynb` | AISQL関数（SENTIMENT、AI_CLASSIFY等） | `Scripts/vignette-4-aisql(Appendix).sql` |
| `vignette-4-copilot.ipynb` | Snowflake Copilotの使用方法 | `Scripts/vignette-4-copilot(Appendix).sql` |
| `vignette-5-governance.ipynb` | Horizonによるガバナンス機能 | `Scripts/vignette-5(appendix).sql` |

## 🚀 使い方

### Snowflake Notebookでの実行

1. Snowflakeアカウントにログイン
2. 「Projects」→「Notebooks」に移動
3. 「Import .ipynb file」をクリック
4. このフォルダから任意の`.ipynb`ファイルを選択
5. セルを順番に実行

### SQLマジックコマンド

各コードセルには`%%sql`マジックコマンドが含まれており、SQLをSnowflakeで直接実行できます。

```python
%%sql
USE DATABASE tb_101;
USE ROLE accountadmin;
```

## 📝 実行順序

推奨される実行順序：

1. **setup.ipynb** - 最初に実行（データベースとウェアハウスの作成）
2. **vignette-1.ipynb** - ウェアハウスとリソース管理の基礎
3. **vignette-2.ipynb** - データパイプラインの構築
4. **vignette-3.ipynb** - Marketplaceデータの統合
5. **vignette-4-aisql.ipynb** - AI関数の活用
6. **vignette-4-copilot.ipynb** - Copilotによるクエリ作成
7. **vignette-5-governance.ipynb** - ガバナンスとセキュリティ

## ⚠️ 注意事項

- 各Notebookは独立して実行できますが、`setup.ipynb`を先に実行することを推奨します
- 一部のNotebookはSnowflake Marketplaceからのデータ（Weather Source、Safegraph）が必要です
- クリーンアップセルは必要に応じて実行してください
- Snowflakeアカウントの適切な権限（ACCOUNTADMIN等）が必要な場合があります

## 🔗 リソース

- [Snowflake Documentation](https://docs.snowflake.com/)
- [Snowflake Notebooks](https://docs.snowflake.com/en/user-guide/ui-snowsight-notebooks)
- [Tasty Bytes Quickstart](https://quickstarts.snowflake.com/guide/tasty_bytes_introduction/)

## 📂 フォルダ構造

```
zero_to_snowflake/
├── Scripts/              # 元のSQLスクリプト
├── Notebook/            # このフォルダ（Notebook版）
│   ├── setup.ipynb
│   ├── vignette-1.ipynb
│   ├── vignette-2.ipynb
│   ├── vignette-3.ipynb
│   ├── vignette-4-aisql.ipynb
│   ├── vignette-4-copilot.ipynb
│   ├── vignette-5-governance.ipynb
│   └── README.md
└── streamlit/           # Streamlitアプリケーション
```

## 💡 ヒント

- セルを個別に実行して、各ステップの結果を確認できます
- エラーが発生した場合は、前のセルが正常に実行されたか確認してください
- 長時間実行されるクエリがある場合は、ウェアハウスのサイズを調整してください
- 各Notebookの最後にクリーンアップセルがあり、リソースを解放できます

