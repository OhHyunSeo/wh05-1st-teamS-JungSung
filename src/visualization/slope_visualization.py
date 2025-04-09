'''경사도 상위 50% 지도배경 시각화 '''

import koreanize_matplotlib
import osmnx as ox
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import contextily as ctx

# 1. 광진구 행정 경계 가져오기 및 미터 좌표계로 변환 (EPSG:5174 사용)
place_name = "Gwangjin-gu, Seoul, South Korea"
gwangjin = ox.geocode_to_gdf(place_name)
gwangjin_meter = gwangjin.to_crs(epsg=5174)

# 2. 표고 데이터 불러오기 ("N3P_F002.shp")
#    파일은 고도 정보(HEIGHT 속성)를 포함한다고 가정합니다.
elev = gpd.read_file("./shp/N3P_F002.shp")
elev = elev.to_crs(epsg=5174)
# 광진구 영역 내로 클리핑
elev_clip = gpd.clip(elev, gwangjin_meter)

# 3. 100m 격자 데이터 불러오기 ("100m격자.shp")
grid = gpd.read_file("./shp/100m.shp")
grid = grid.to_crs(epsg=5174)
# 광진구 영역 내 격자만 남김
grid_clip = gpd.clip(grid, gwangjin_meter)

# 4. 각 격자 셀별 경사도 계산
#    - 각 셀 내 표고 데이터의 HEIGHT 값 범위를 이용
#    - 100m 격자의 대각선 길이: √(100² + 100²) ≈ 141.42 m
cell_size = 100  # m
cell_diag = np.sqrt(cell_size**2 + cell_size**2)  # 약 141.42 m

slope_list = []
for idx, cell in grid_clip.iterrows():
    # 격자 셀 내 표고 데이터 클리핑
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

# (선택) 전체 셀에 대한 경사도 히트맵 시각화
fig, ax = plt.subplots(figsize=(12, 12))
gwangjin_plot.boundary.plot(ax=ax, color='black', linewidth=2)
grid_plot.plot(ax=ax, column="slope_deg", cmap="Blues", edgecolor='grey', linewidth=0.5, legend=True)
plt.title("광진구 지역 경사도 (표고 데이터 기반, 100m 격자, Blues 컬러맵)")
plt.xlabel("경도")
plt.ylabel("위도")
plt.show()

# 6. 경사도가 높은 순 상위 50% 셀 추출하기
sorted_cells = grid_plot.sort_values(by="slope_deg", ascending=False).reset_index(drop=True)
n_top = int(len(sorted_cells) * 0.5)
top_cells = sorted_cells.head(n_top)

# GID 필드가 없으면 인덱스를 GID로 사용 (shapefile에 GID 필드가 있다면 생략)
if "GID" not in top_cells.columns:
    top_cells["GID"] = top_cells.index

# 7. 각 격자 셀 중심(centroid) 좌표 계산 (EPSG:4326: 경도=x, 위도=y)
top_cells["centroid"] = top_cells.geometry.centroid
top_cells["centroid_lon"] = top_cells["centroid"].apply(lambda point: point.x)
top_cells["centroid_lat"] = top_cells["centroid"].apply(lambda point: point.y)

# 결과 DataFrame (GID, 중심 좌표)
result = top_cells[["GID", "centroid_lat", "centroid_lon"]]
print("경사도 상위 50% 셀의 GID(위도, 경도) 정보:")
print(result)

# 8. contextily를 이용해서 배경지도 추가 후 상위 50% 셀 시각화 (Reds 컬러맵)
# contextily는 EPSG:3857 (Web Mercator)을 사용하므로 재투영합니다.
gwangjin_3857 = gwangjin_plot.to_crs(epsg=3857)
top_cells_3857 = top_cells.to_crs(epsg=3857)

fig, ax = plt.subplots(figsize=(12, 12))
# 광진구 행정 경계 표시
gwangjin_3857.boundary.plot(ax=ax, color='black', linewidth=2)
# 상위 50% 셀 시각화 (Reds 컬러맵)
top_cells_3857.plot(ax=ax, column="slope_deg", cmap="Reds", edgecolor='grey', linewidth=0.5, legend=True)
# contextily 배경지도 추가 (여기서는 OpenStreetMap Mapnik 사용)
ctx.add_basemap(ax, crs=top_cells_3857.crs, source=ctx.providers.OpenStreetMap.Mapnik)

plt.title("광진구 상위 50% 경사도 셀 시각화 (Reds 컬러맵 + 배경지도)")
plt.xlabel("경도")
plt.ylabel("위도")
plt.show()