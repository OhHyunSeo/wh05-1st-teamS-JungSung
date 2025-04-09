'''시각화한 자료에서 경사도가 높은 상위 50% 좌표 추출 코드'''
import koreanize_matplotlib
import osmnx as ox
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np

# 1. 광진구 행정 경계 가져오기 및 미터 좌표계로 변환 (EPSG:5174 사용)
place_name = "Gwangjin-gu, Seoul, South Korea"
gwangjin = ox.geocode_to_gdf(place_name)
gwangjin_meter = gwangjin.to_crs(epsg=5174)

# 2. 표고 데이터 불러오기 ("N3P_F002.shp")
#    파일은 고도 정보(HEIGHT 속성)를 포함한다고 가정합니다.
elev = gpd.read_file("./shp/N3P_F002.shp")
elev = elev.to_crs(epsg=5174)
# 광진구 영역 내로만 클리핑
elev_clip = gpd.clip(elev, gwangjin_meter)

# 3. 100m 격자 데이터 불러오기 ("100m격자.shp")
grid = gpd.read_file("./shp/100m.shp")
grid = grid.to_crs(epsg=5174)
# 광진구 영역 내 격자만 남김
grid_clip = gpd.clip(grid, gwangjin_meter)

# 4. 각 격자 셀별 경사도 계산
#    - 각 셀 내 표고 데이터의 HEIGHT 범위를 이용
#    - 100m 격자의 대각선 길이: √(100² + 100²) ≈ 141.42 m
cell_size = 100
cell_diag = np.sqrt(cell_size**2 + cell_size**2)

slope_list = []
for idx, cell in grid_clip.iterrows():
    elev_in_cell = gpd.clip(elev_clip, cell.geometry)
    if elev_in_cell.empty:
        slope_list.append(0)
    else:
        heights = elev_in_cell["HEIGHT"]
        if heights.empty:
            slope_list.append(0)
        else:
            elev_range = heights.max() - heights.min()
            slope_rad = np.arctan(elev_range / cell_diag)
            slope_deg = np.degrees(slope_rad)
            slope_list.append(slope_deg)

grid_clip["slope_deg"] = slope_list

# 5. 시각화를 위한 좌표계 재투영 (EPSG:4326)
grid_plot = grid_clip.to_crs(epsg=4326)
gwangjin_plot = gwangjin.to_crs(epsg=4326)

# 6. 경사도 히트맵 시각화 (Blues 컬러맵)
fig, ax = plt.subplots(figsize=(12, 12))
gwangjin_plot.boundary.plot(ax=ax, color='black', linewidth=2)
grid_plot.plot(ax=ax, column="slope_deg", cmap="Blues", edgecolor='grey', linewidth=0.5, legend=True)
plt.title("광진구 지역 경사도 (표고 데이터 기반, 100m 격자, Blues 컬러맵)")
plt.xlabel("경도")
plt.ylabel("위도")
plt.show()

# 7. 원본 격자 파일에 존재하는 GID 필드 사용 결정 (대소문자 구분)
if "GID" in grid_clip.columns:
    gid_field = "GID"
elif "gid" in grid_clip.columns:
    gid_field = "gid"
else:
    gid_field = None

# 8. 중앙값 기준 상위 50% 셀 추출
median_slope = grid_plot["slope_deg"].median()
top_cells = grid_plot[grid_plot["slope_deg"] >= median_slope].copy()

# GID 필드를 그대로 사용(다사xxxx 형식), 없으면 인덱스를 사용
if gid_field is not None:
    top_cells["GID"] = top_cells[gid_field].astype(str)
else:
    top_cells["GID"] = top_cells.index.astype(str)

# 9. 각 셀 중심 좌표(경도=centroid.x, 위도=centroid.y) 계산
top_cells["centroid"] = top_cells.geometry.centroid
top_cells["centroid_lon"] = top_cells["centroid"].apply(lambda p: p.x)
top_cells["centroid_lat"] = top_cells["centroid"].apply(lambda p: p.y)

# 10. 결과: GID(다사xxxx), 위도, 경도
result = top_cells[["GID", "centroid_lat", "centroid_lon"]]
print("경사도 상위 50% 셀의 GID(다사xxxx) 및 좌표:")
print(result)

# CSV로 저장 - UTF-8 BOM 추가(Excel 호환)
result.to_csv("top50.csv", index=False, encoding="utf-8-sig")