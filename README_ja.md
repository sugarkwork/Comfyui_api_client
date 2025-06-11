# ComfyUI API クライアント

ComfyUI API との連携を行うPythonクライアントライブラリです。同期・非同期両方の操作をサポートし、ワークフローフォーマットの自動変換機能を備えています。

## 特徴

- 🔄 **デュアルクライアント対応**: 同期（`ComfyUIClient`）と非同期（`ComfyUIClientAsync`）の両実装
- 🎯 **自動フォーマット検出**: `workflow.json`を自動的にAPIフォーマットに変換
- 🛠️ **拡張設定機能**: あらゆるパラメータタイプに対応した柔軟な`set_data()`メソッド
- 🐛 **デバッグモード**: 開発とトラブルシューティング用のオプションデバッグ出力
- 🔧 **動的リロード**: 再起動なしでワークフローファイルをリロード
- 🛡️ **堅牢なエラーハンドリング**: ユーザーフレンドリーなメッセージを持つ包括的エラー処理
- 🔍 **スマートノード検索**: タイトルまたはclass_typeでノードを検索
- 📦 **画像アップロード対応**: ComfyUIサーバーへの直接画像アップロード

## インストール

```bash
pip install -r requirements.txt
```

### 依存関係

```
requests
aiohttp
Pillow
```

## クイックスタート

### 同期クライアント

```python
from comfyuiclient import ComfyUIClient

# クライアントを初期化（workflow.jsonとworkflow_api.jsonの両方に対応）
client = ComfyUIClient("localhost:8188", "workflow.json")
client.connect()

# パラメータを設定
client.set_data(key='KSampler', seed=12345)
client.set_data(key='CLIP Text Encode Positive', text="美しい風景")

# 画像を生成
results = client.generate(["Result Image"])
for key, image in results.items():
    image.save(f"{key}.png")

client.close()
```

### 非同期クライアント

```python
import asyncio
from comfyuiclient import ComfyUIClientAsync

async def main():
    # 非同期クライアントを初期化
    client = ComfyUIClientAsync("localhost:8188", "workflow.json")
    await client.connect()
    
    # パラメータを設定（すべて非同期）
    await client.set_data(key='KSampler', seed=12345)
    await client.set_data(key='CLIP Text Encode Positive', text="美しい風景")
    
    # 画像を生成
    results = await client.generate(["Result Image"])
    for key, image in results.items():
        image.save(f"{key}.png")
    
    await client.close()

asyncio.run(main())
```

## APIリファレンス

### クライアントの初期化

```python
# 基本的な初期化
client = ComfyUIClient(server_address, workflow_file)

# デバッグモード付き
client = ComfyUIClient(server_address, workflow_file, debug=True)
```

**パラメータ:**
- `server_address`: ComfyUIサーバーのアドレス（例："localhost:8188"）
- `workflow_file`: workflow.jsonまたはworkflow_api.jsonのパス
- `debug`: デバッグ出力を有効にする（デフォルト：False）

### 主要メソッド

#### `connect()`
ComfyUIサーバーへの接続を確立します。

```python
# 同期
client.connect()

# 非同期
await client.connect()
```

#### `set_data(key, **kwargs)`
ワークフローノードのパラメータを設定します。

```python
# 基本パラメータ
client.set_data(key='KSampler', seed=12345)
client.set_data(key='CLIP Text Encode Positive', text="プロンプトテキスト")

# 高度なパラメータ
client.set_data(key='KSampler', input_key='steps', input_value=25)
client.set_data(key='EmptyLatentImage', number=512.0)
client.set_data(key='SomeNode', value=1.5)

# 画像アップロード
from PIL import Image
image = Image.open("input.png")
client.set_data(key='LoadImage', image=image)
```

**パラメータ:**
- `key`: ノードタイトルまたはclass_type
- `text`: テキストノード用のテキスト入力
- `seed`: 生成ノード用のシード値
- `image`: 画像入力用のPIL Imageオブジェクト
- `number`: 数値パラメータ（'Number'入力にマップ）
- `value`: 数値パラメータ（'value'入力にマップ）
- `input_key`/`input_value`: 任意のキー値ペア

#### `generate(node_names=None)`
指定されたノードから出力を生成します。

```python
# 特定のノードから生成
results = client.generate(["Result Image", "Preview"])

# すべての出力ノードから生成
results = client.generate()

# 結果は{node_name: PIL.Image}辞書として返される
for node_name, image in results.items():
    image.save(f"{node_name}.png")
```

#### `reload()`
ワークフローファイルをリロードします（動的ワークフローに便利）。

```python
client.reload()
```

#### `close()`
接続を閉じ、リソースをクリーンアップします。

```python
# 同期
client.close()

# 非同期
await client.close()
```

### ユーティリティ関数

#### `convert_workflow_to_api(workflow_json)`
ComfyUIワークフローフォーマットをAPIフォーマットに変換します。

```python
from comfyuiclient import convert_workflow_to_api

# ファイルを変換
api_format = convert_workflow_to_api("workflow.json")

# 辞書を変換
with open("workflow.json") as f:
    workflow_data = json.load(f)
api_format = convert_workflow_to_api(workflow_data)
```

## ワークフローファイル対応

クライアントは両方のワークフローフォーマットを自動検出して処理します：

### workflow.json（ComfyUIエディタフォーマット）
- ComfyUI Webインターフェースからエクスポート
- UIレイアウトと視覚情報を含む
- **自動的にAPIフォーマットに変換**

### workflow_api.json（ComfyUI APIフォーマット）
- API対応フォーマット
- **変換なしで直接使用**

自動検出の例：
```python
# どちらもシームレスに動作
client1 = ComfyUIClient("localhost:8188", "workflow.json")      # 自動変換
client2 = ComfyUIClient("localhost:8188", "workflow_api.json")  # 直接使用
```

## エラーハンドリング

クライアントは包括的なエラーハンドリングを提供します：

```python
try:
    client = ComfyUIClient("localhost:8188", "workflow.json")
    client.connect()
    results = client.generate(["Result Image"])
except ConnectionError as e:
    print(f"接続に失敗しました: {e}")
except ValueError as e:
    print(f"無効なデータです: {e}")
except TimeoutError as e:
    print(f"操作がタイムアウトしました: {e}")
except Exception as e:
    print(f"予期しないエラー: {e}")
finally:
    client.close()
```

## デバッグモード

詳細なログ出力を行うためにデバッグモードを有効にします：

```python
client = ComfyUIClient("localhost:8188", "workflow.json", debug=True)
```

デバッグ出力に含まれるもの：
- ワークフロー読み込みステータス
- パラメータ設定の詳細
- ノード検索情報
- エラーの詳細とリトライ試行

## 高度な使用例

### コンテキストマネージャーパターン

```python
class ComfyUIContextManager:
    def __init__(self, *args, **kwargs):
        self.client = ComfyUIClient(*args, **kwargs)
    
    def __enter__(self):
        self.client.connect()
        return self.client
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

# 使用法
with ComfyUIContextManager("localhost:8188", "workflow.json") as client:
    client.set_data(key='KSampler', seed=12345)
    results = client.generate(["Result Image"])
```

### バッチ処理

```python
import random

prompts = ["山に沈む夕日", "夜の街", "森の湖"]
seeds = [random.randint(0, 2**32) for _ in range(3)]

client = ComfyUIClient("localhost:8188", "workflow.json")
client.connect()

for i, (prompt, seed) in enumerate(zip(prompts, seeds)):
    client.set_data(key='CLIP Text Encode Positive', text=prompt)
    client.set_data(key='KSampler', seed=seed)
    
    results = client.generate(["Result Image"])
    for key, image in results.items():
        image.save(f"output_{i}_{key}.png")

client.close()
```

### 動的ワークフロー更新

```python
client = ComfyUIClient("localhost:8188", "workflow.json")
client.connect()

# 初回生成
client.set_data(key='KSampler', seed=12345)
results = client.generate(["Result Image"])

# 外部でワークフローファイルを変更した後、リロード
client.reload()

# 更新されたワークフローを使用
client.set_data(key='KSampler', seed=67890)
results = client.generate(["Result Image"])

client.close()
```

## テスト

テストスイートを実行：

```bash
# 基本機能テスト
python test_workflow_loading.py

# エラーハンドリングテスト
python test_error_handling.py

# 拡張機能テスト
python test_enhanced_features.py

# フォーマット変換テスト
python test_conversion.py
```

## トラブルシューティング

### よくある問題

**1. 接続拒否**
```
ConnectionError: Failed to connect to ComfyUI server
```
- 指定されたアドレスでComfyUIが実行されていることを確認
- ファイアウォール設定を確認
- ポート番号を確認

**2. キーが見つからない**
```
Key not found: NodeName
```
- ComfyUIインターフェースでノードタイトルを確認
- タイトルの代わりにclass_typeを試す
- デバッグモードを有効にして利用可能なノードを確認

**3. タイムアウトエラー**
```
TimeoutError: Timeout waiting for prompt to complete
```
- 複雑なワークフローは5分以上かかる場合がある
- ComfyUIサーバーのパフォーマンスを確認
- ワークフローが有効であることを確認

### デバッグのコツ

1. **デバッグモードを有効にする**詳細ログを取得：
   ```python
   client = ComfyUIClient("localhost:8188", "workflow.json", debug=True)
   ```

2. **ワークフロー内のノード名を確認**：
   ```python
   client = ComfyUIClient("localhost:8188", "workflow.json", debug=True)
   # デバッグ出力で利用可能なノードIDとタイトルが表示される
   ```

3. **クライアントを使用する前にComfyUIでワークフローをテスト**

4. **フォーマット変換を使用してワークフローを理解**：
   ```python
   api_format = convert_workflow_to_api("workflow.json")
   print(json.dumps(api_format, indent=2))
   ```

## 実用的な使用例

### AI画像生成パイプライン

```python
import random
from comfyuiclient import ComfyUIClient

def generate_artwork(prompt, style="realistic", steps=20):
    """AI アートワーク生成関数"""
    client = ComfyUIClient("localhost:8188", "workflow.json")
    client.connect()
    
    try:
        # プロンプトとスタイルを設定
        full_prompt = f"{prompt}, {style} style"
        client.set_data(key='CLIP Text Encode Positive', text=full_prompt)
        client.set_data(key='KSampler', seed=random.randint(0, 2**32))
        client.set_data(key='KSampler', input_key='steps', input_value=steps)
        
        # 画像生成
        results = client.generate(["Result Image"])
        
        return list(results.values())[0]  # 最初の画像を返す
    finally:
        client.close()

# 使用例
image = generate_artwork("桜咲く日本庭園", "anime", 25)
image.save("japanese_garden.png")
```

### バッチ画像生成システム

```python
import asyncio
from comfyuiclient import ComfyUIClientAsync

async def batch_generate(prompts, output_dir="outputs"):
    """複数プロンプトの一括生成"""
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    client = ComfyUIClientAsync("localhost:8188", "workflow.json")
    await client.connect()
    
    try:
        for i, prompt in enumerate(prompts):
            print(f"生成中 {i+1}/{len(prompts)}: {prompt}")
            
            await client.set_data(key='CLIP Text Encode Positive', text=prompt)
            await client.set_data(key='KSampler', seed=i * 1000)
            
            results = await client.generate(["Result Image"])
            
            for key, image in results.items():
                filename = f"{output_dir}/image_{i:03d}_{key}.png"
                image.save(filename)
                print(f"保存完了: {filename}")
    finally:
        await client.close()

# 使用例
prompts = [
    "美しい夕焼けの海岸",
    "雪山の頂上から見る景色",
    "都市の夜景",
    "森の中の小さな家"
]

asyncio.run(batch_generate(prompts))
```

### 画像バリエーション生成

```python
def create_variations(base_prompt, variations, count=4):
    """ベースプロンプトから複数のバリエーションを生成"""
    client = ComfyUIClient("localhost:8188", "workflow.json")
    client.connect()
    
    all_images = []
    
    try:
        for var in variations:
            for i in range(count):
                prompt = f"{base_prompt}, {var}"
                
                client.set_data(key='CLIP Text Encode Positive', text=prompt)
                client.set_data(key='KSampler', seed=random.randint(0, 2**32))
                
                results = client.generate(["Result Image"])
                
                for key, image in results.items():
                    filename = f"{var}_{i+1}.png"
                    image.save(filename)
                    all_images.append((filename, image))
                    
    finally:
        client.close()
    
    return all_images

# 使用例
base = "ファンタジーの風景"
variations = ["朝の光", "夕暮れ", "星空", "雨の日"]
images = create_variations(base, variations, 2)

print(f"合計 {len(images)} 枚の画像を生成しました")
```

## ライセンス

このプロジェクトはMITライセンスのもとでライセンスされています - 詳細はLICENSEファイルを参照してください。

## 貢献

1. リポジトリをフォーク
2. フィーチャーブランチを作成
3. 新機能にテストを追加
4. すべてのテストが通ることを確認
5. プルリクエストを提出

## 変更履歴

### 最新バージョン
- ✅ 特定の例外タイプを持つ拡張エラーハンドリング
- ✅ 開発とトラブルシューティング用のデバッグモード
- ✅ workflow.jsonからAPIフォーマットへの自動変換
- ✅ 動的ワークフローリロード
- ✅ 任意パラメータサポートを持つ拡張set_data()
- ✅ タイトルまたはclass_typeによるスマートノード検索
- ✅ 包括的テストスイート
- ✅ 長時間実行操作のタイムアウト処理
- ✅ 堅牢なリソースクリーンアップ

## サポート

質問や問題がある場合は、GitHubのIssuesページで報告してください。

## 関連リンク

- [ComfyUI公式リポジトリ](https://github.com/comfyanonymous/ComfyUI)
- [ComfyUI API ドキュメント](https://docs.comfy.org/essentials/comfyui_api)
- [Python Pillow ドキュメント](https://pillow.readthedocs.io/)