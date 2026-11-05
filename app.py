from flask import Flask, jsonify, request
from flask_cors import CORS
from geopy.distance import geodesic

app = Flask(__name__)
CORS(app) # フロントエンドからの通信を許可

# 名護市内の主要スポットの座標データ（ダミー）
SPOTS = {
    "pineapple_park": {"lat": 26.6322, "lon": 127.9678, "name": "ナゴパイナップルパーク"}
}

@app.route('/')
def home():
    return jsonify({"status": "名護RPG バックエンド稼働中！"})

# GPSとQR判定のAPI
@app.route('/api/checkin', methods=['POST'])
def checkin():
    data = request.json
    spot_id = data.get('spot_id')
    user_lat = data.get('lat')
    user_lon = data.get('lon')

    if spot_id not in SPOTS:
        return jsonify({"success": False, "message": "存在しないスポットです"}), 400

    target = SPOTS[spot_id]
    target_coords = (target['lat'], target['lon'])
    user_coords = (user_lat, user_lon)

    # 距離（メートル）を計算
    distance = geodesic(target_coords, user_coords).meters

    # 100m以内にいれば判定OK
    if distance <= 100:
        return jsonify({
            "success": True,
            "message": f"{target['name']}へのチェックイン成功！",
            "next_unlock": "名桜ボウル"
        })
    else:
        return jsonify({
            "success": False,
            "message": f"スポットから遠すぎます（現在地から約{int(distance)}m）"
        })

# ★ここが重要です！この2行がないと起動しません★


if __name__ == '__main__':
    # host='0.0.0.0' にすると、同じネットワーク内の他の端末からアクセス可能になります
    app.run(host='0.0.0.0', port=5000, debug=True)