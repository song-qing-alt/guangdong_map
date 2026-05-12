import json
from pathlib import Path

# data 文件夹路径
data_dir = Path("data")

# 查找所有城市的村/居委会点位文件
# 例如：guangzhou_village_point.geojson、foshan_village_point.geojson
point_files = sorted(data_dir.glob("*_village_point.geojson"))

all_features = []

print("开始合并村/居委会点位文件...")
print("-" * 50)

for file in point_files:
    print(f"正在读取：{file.name}")

    with open(file, "r", encoding="utf-8") as f:
        geojson = json.load(f)

    features = geojson.get("features", [])

    # 给每个点位加一个来源城市字段，方便后期查询
    city_name = file.name.replace("_village_point.geojson", "")

    for feature in features:
        if "properties" not in feature or feature["properties"] is None:
            feature["properties"] = {}
        feature["properties"]["source_city"] = city_name

    all_features.extend(features)

# 合并后的 GeoJSON
merged_geojson = {
    "type": "FeatureCollection",
    "features": all_features
}

# 输出文件
output_file = data_dir / "village_points.geojson"

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(merged_geojson, f, ensure_ascii=False)

print("-" * 50)
print("合并完成！")
print(f"合并文件数量：{len(point_files)}")
print(f"合并点位数量：{len(all_features)}")
print(f"输出文件：{output_file}")