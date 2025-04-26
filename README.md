# Copilot-Shooter

GitHub Copilot と Pyxel で作成したサンプルシューティングゲームです。

デモ : [https://yamagame.github.io/copilot-shooter](https://yamagame.github.io/copilot-shooter)

以下、作成に使用したChat。モデルは ChatGPT 4o。
多少手直ししてるものの、ほぼコピペ

- shooter/shooter.py を書き換えて Pyxel で書かれたシューティングゲームを作って
- PlayerとBulletとEnemyを別のクラスにして
- Enemeyを画面を左右に往復するように動かして
- EnemyにBulletが当たったら再出現するように変更
- Enemyが弾を撃ってくるように変更、Enemyの弾はPlayerを狙って飛んでくること
- それぞれのクラスを別々のファイルにして
- EnemyBulletをランダムに発射するように変更
- タイトルとゲームオーバー画面を追加
- 隕石を画面上部から出現、隕石は画面上から下へ向かって移動、画面上に最大5個まで同時表示
- MeteorにBulletがヒットするように変更、MeteorはBulletが当たっても壊れない
- EnemyにBulletがヒットしたら、破片が散らばるように
- 背景に星を上から下へ流す
- Enemy爆発時とBullet発射時に効果音を鳴らす
- Enemy_BulletがPlayerにヒットしたら、派手に爆発
- PayerにEnemy_Bulletがヒットしたときに出現するFragmentが画面から消えるまでゲームオーバーへ遷移しないように
- EXPLODINGステートになったら、Playerを非表示に
- ゲームオーバー画面やタイトル画面でもStarが動くように
- ゲームオーバー画面でRキーを押さなくても、一定時間でタイトルへ遷移するように
- ENEMEYを倒す毎に、画面上のMETEORの数を一つずつ増やして、最大100個まで表示できるように
- METEORが左右に30ピクセルほど、sinカーブを描くように移動するように変更
- ベストスコアの表示
- ゲーム中もベストスコアを表示する
- タイトルをCopilot-Shooterに変更
- ゲーム中、ベストスコアを更新するように
