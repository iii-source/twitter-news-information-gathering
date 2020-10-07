# twitter-news-information-gathering

### TwitterAPIを利用し任意の情報を収集するアプリケーションです。
- https://iii-source.github.io/public/swagger_ui/tweet_news/docs/dist/
  - twitter-news-information-gatheringのAPI設計書を公開してます。

- https://iii-source.github.io/public/twitter-news-information-gathering/
  - twitter-news-information-gatheringの設計書(シーケンス図等)を公開してます。

---

#### 以下、使用している技術、工夫点
- JSON Schemaによるvalidationチェック
  - APIのパラメーターをチェックし、必要な値がなかった場合はエラーを返します。
  - APIの利用者は戻り値にjsonデータを期待することから、
  エラーレスポンスは極力jsonデータで返却するように設定してます。
  - 必要なAPIエンドポイントにデコレーターを使用し、必要なvalidationチェックを
  外部に実装することでAPIエンドポイントの可読性を向上を工夫してます。

- Pytestによる単体テストの自動化
  - テストを自動化させ、改修した際のデグレを検知しやすくすることを目的で実装しました。
  - 事前にデータを準備する必要のあるテストはfixtureを使用しテストコード本体の
  可読性を上げました。
  - parameterizedを使用し複数のテストパターンを網羅する際、
  そのテストケース分必要なパラメーターを外出しし、保守性の向上を意識しました。
  - 共通処理(APIのGET,POST等)は1つに集約し保守性を上げました。

- HTTPBasicAuthによる認証機能とuuidを使用した認可機能の実装
  - Basic64を使用しuser,password認証を実装しセキュリティ面で
  必要事項を考慮しました。
  - 認証後、権限のあるuuidを発行し認可してます。
