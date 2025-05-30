# ❄️ 보행 취약 계층 보호 및 제설 사각지대 해소를 위한 열선 설치 입지 분석

---

## 📌 프로젝트 개요

- **프로젝트명**: 보행 취약 계층 보호 및 제설 사각지대 해소를 위한 열선 설치 입지 분석
- **프로젝트 목표**:  
  겨울철 낙상사고와 결빙 사고로부터 보행 약자를 보호하고, 제설 사각지대를 줄이기 위한 **지자체 기반의 데이터 분석 및 의사결정 지원 서비스 개발**

### 🔁 프로젝트 흐름도

<p align='center'>
  <img src="https://github.com/user-attachments/assets/cada2586-1282-40ed-999a-521b971827db" alt="Flow Chart" width="300"/>
</p>

---

## 🗓️ 프로젝트 일정

| 작업 항목                      | 시작일     | 종료일     | 기간(일) |
| ------------------------------ | ---------- | ---------- | -------- |
| 주제 정의 및 계획 수립         | 2025-03-12 | 2025-03-17 | 6일      |
| 아이디어 도출 및 시나리오 작성 | 2025-03-17 | 2025-03-19 | 3일      |
| 데이터 수집 및 전처리          | 2025-03-19 | 2025-03-25 | 7일      |
| 요구사항 도출 및 WBS 작성      | 2025-03-25 | 2025-03-25 | 1일      |
| 결빙 판단 알고리즘 적용        | 2025-03-21 | 2025-03-24 | 4일      |
| 최종 검토 및 발표 준비         | 2025-03-24 | 2025-03-26 | 3일      |
| 프로젝트 발표                  | 2025-03-26 | 2025-03-26 | 1일      |

---

## ⚙️ 작업 분할 구조 (WBS)

### 1단계: 기획

- **문제 정의**
  - 겨울철 보행자 낙상 및 결빙 사고 현황 분석
  - 보행 취약 계층 보호 필요성과 기존 대응 한계 파악
- **데이터 요구사항 정의**
  - 교통량, 기상, GIS, 유동 인구, 기존 열선 설치 구역 등
  - 공공 데이터 포털, API, 지자체 직접 요청 등으로 접근

### 2단계: 데이터 수집 및 준비

- **데이터 수집**
  - 기상청 API, 수동 다운로드
  - MySQL / Google Drive 데이터 저장소 구성
- **데이터 전처리**
  - 결측치·이상치 처리
  - 격자형 통일 및 데이터 클렌징

### 3단계: 분석 및 모델링

- **시각화**
  - `matplotlib`, `seaborn`, `folium` 등 활용
- **결빙 판단 알고리즘 적용**
  - 관련 논문 기반 알고리즘 도입
- **결과 평가**
  - 총 5가지 상황별 결빙 판단 알고리즘 비교 분석

---

## 🧊 결빙 판단 알고리즘

| 알고리즘 유형 | 설명                                 | Flow Chart                                                                                                         |
| ------------- | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------ |
| 1. 응결 결빙  | 대기 중 수증기 → 지면에서 응결       | <p align='center'><img src="https://github.com/user-attachments/assets/2eca4fe4-d522-4b1d-9932-8a3426490562"/></p> |
| 2. 강수 결빙  | 비나 진눈깨비가 내려 얼어붙는 상황   | <p align='center'><img src="https://github.com/user-attachments/assets/e00d165b-7003-4e41-a255-e9227bb086cd"/></p> |
| 3. 적설 결빙  | 눈이 내린 후 얼어붙는 상태           | <p align='center'><img src="https://github.com/user-attachments/assets/6e57c381-0874-4408-8e69-267c239a81b6"/></p> |
| 4. 결빙 지속  | 일정 시간 동안 기온 유지 → 결빙 지속 | <p align='center'><img src="https://github.com/user-attachments/assets/76bac1a1-540a-4399-b6f0-0abb7ea60a7f"/></p> |
| 5. 풍속 영향  | 풍속이 결빙에 영향을 주는 경우       | <p align='center'><img src="https://github.com/user-attachments/assets/09d09f0e-07fa-48f5-bb30-63513002e1c5"/></p> |

---

## 🛠️ 시스템 설계 및 기술 스택

### 시스템 아키텍처

1. **데이터 수집 모듈**
   - 교통/기상/GIS 등 다양한 소스에서 수집
   - API 호출 및 자동화 수집 포함
2. **전처리 모듈**
   - 결측치 처리 및 격자 단위 통일
3. **분석 및 시각화 모듈**
   - 알고리즘 기반 결빙 판단
   - 대시보드 및 시각 자료 생성

### 기술 스택

| 목적       | 기술                                                    |
| ---------- | ------------------------------------------------------- |
| **수집**   | Python, QGIS, API                                       |
| **분석**   | Pandas, NumPy, Scikit-learn, TensorFlow                 |
| **시각화** | Matplotlib, Seaborn, Plotly, Geopython, Polygon, Folium |

---

## 🚨 예상 문제 및 해결 방안

| 문제                                | 해결 방안                               |
| ----------------------------------- | --------------------------------------- |
| 격자 단위 불일치 (데이터 타입 상이) | `folium`을 활용한 중심점 정렬 및 일치화 |
