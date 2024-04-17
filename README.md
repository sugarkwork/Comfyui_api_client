# Comfyui_api_client
ComfyUI の API にデータを投げやすくするだけのクラスです。

普通版（ComfyUiClient）と、async 版（ComfyUiClientAsync）があります。

特徴としては、ノード名を自動で探して、データを入れてくれる set_data メソッドです。

例えば、CLIP Text Encode Positive というタイトルを付けたノードがあり、そこのテキスト部分にテキストを入れたい場合

    comfyui_client.set_data(key='CLIP Text Encode Positive', text="beautiful landscape painting")
    
こう指定する事で、該当ノードの text 部分にテキストを入れられます。

set_data には複数の引数があり、text, seed, image が受け取れます。image は、PIL.Image 型の画像を受け取ってサーバーにアップロードしてパラメータをセットします。これは Load Image ノードの利用を想定しています。

    comfyui_client.set_data(key='Load Image', image=Image.open(input_image_file))

また生成された画像を保存するときは、

    comfyui_client.generate(["Result Image"])
    
この generate メソッドに配列として、ノードの名前を指定する事で、画像を取り出せます。

従って、ワークフローを作る時に、取り出したい画像はノード名を固有の分かりやすい名前にしておく必要があります。

返り値は、ノード名と画像（PIL.Image）のペアなので、適宜取り出して処理出来ます。

# Sample

    comfyui_client = None
    try:
        comfyui_client = ComfyUIClient("127.0.0.1:8188", "workflow_api.json")
        comfyui_client.connect()
        comfyui_client.set_data(key='KSampler', seed=random.randint(0, sys.maxsize))
        comfyui_client.set_data(key='CLIP Text Encode Positive', text="beautiful landscape painting")
        for key, image in comfyui_client.generate(["Result Image"]).items():
            image.save(f"{key}.png")
            print(f"Saved {key}.png")
    finally:
        if comfyui_client is not None:
            comfyui_client.close()

# Sample Async
    comfyui_client = None
    try:
        comfyui_client = ComfyUIClientAsync("127.0.0.1:8188", "workflow_api.json")
        await comfyui_client.connect()
        comfyui_client.set_data(key='KSampler', seed=random.randint(0, sys.maxsize))
        comfyui_client.set_data(key='CLIP Text Encode Positive', text="beautiful landscape painting")
        for key, image in (await comfyui_client.generate(["Result Image"])).items():
            image.save(f"{key}_async.png")
            print(f"Saved {key}_async.png")
    finally:
        if comfyui_client is not None:
            await comfyui_client.close()
