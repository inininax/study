# 03. 데이터 분석 (NumPy/Pandas)

## 🎯 학습 목표
- NumPy 로 수치 배열을 다룬다
- Pandas 로 데이터프레임을 조작한다
- Matplotlib/Seaborn 으로 시각화한다
- 실전 데이터 분석 워크플로우를 안다

## 1. NumPy 기초

### 1.1 설치 및 임포트
```bash
pip install numpy
```

```python
import numpy as np
```

### 1.2 배열 생성
```python
# 리스트에서
a = np.array([1, 2, 3, 4, 5])

# 2차원
m = np.array([[1, 2, 3], [4, 5, 6]])

# 특별한 배열
zeros = np.zeros((3, 4))         # 3x4 영행렬
ones = np.ones((2, 3))            # 1로 채움
identity = np.eye(3)              # 단위행렬
empty = np.empty((2, 2))          # 초기화 안 함

# 범위
arr = np.arange(10)               # [0, 1, ..., 9]
arr = np.arange(0, 1, 0.1)        # [0, 0.1, ..., 0.9]
arr = np.linspace(0, 1, 5)        # [0, 0.25, 0.5, 0.75, 1]

# 난수
rng = np.random.default_rng(seed=42)
random = rng.random((3, 3))       # 0-1
randint = rng.integers(1, 100, (3, 3))
normal = rng.normal(0, 1, 100)    # 정규분포
```

### 1.3 배열 속성
```python
arr = np.array([[1, 2, 3], [4, 5, 6]])

print(arr.shape)      # (2, 3)
print(arr.ndim)       # 2 (차원)
print(arr.size)       # 6 (요소 개수)
print(arr.dtype)      # int64
print(arr.itemsize)   # 8 (바이트)
```

### 1.4 인덱싱과 슬라이싱
```python
arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# 단일 요소
print(arr[0, 0])       # 1
print(arr[1, 2])       # 6

# 슬라이싱
print(arr[0])          # [1 2 3] (첫 행)
print(arr[:, 0])       # [1 4 7] (첫 열)
print(arr[1:, 1:])     # [[5 6] [8 9]]

# Boolean 인덱싱
mask = arr > 4
print(arr[mask])       # [5 6 7 8 9]

# Fancy 인덱싱
print(arr[[0, 2]])     # 0, 2 행
```

### 1.5 연산 (벡터화)
```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

# 요소별 연산
print(a + b)           # [5 7 9]
print(a * b)           # [4 10 18]
print(a ** 2)          # [1 4 9]

# 스칼라 연산
print(a + 10)          # [11 12 13]
print(a * 2)           # [2 4 6]

# 통계
print(a.sum())         # 6
print(a.mean())        # 2.0
print(a.std())         # 표준편차
print(a.min(), a.max())

# 행렬 연산
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

print(A @ B)           # 행렬 곱
print(A.T)             # 전치
print(np.linalg.inv(A))  # 역행렬
```

### 1.6 형태 변경
```python
arr = np.arange(12)
reshaped = arr.reshape(3, 4)       # 3x4
flattened = reshaped.flatten()     # 1차원
transposed = reshaped.T            # 전치 (4x3)

# 차원 추가
arr = np.array([1, 2, 3])
arr2d = arr[:, np.newaxis]         # (3, 1)
```

### 1.7 브로드캐스팅
서로 다른 크기의 배열도 연산 가능.

```python
a = np.array([[1, 2, 3], [4, 5, 6]])     # (2, 3)
b = np.array([10, 20, 30])               # (3,)

print(a + b)     # 각 행에 b 더함
# [[11 22 33]
#  [14 25 36]]

# 평균 빼기
data = rng.random((100, 5))
centered = data - data.mean(axis=0)
```

## 2. Pandas 기초

### 2.1 설치 및 임포트
```bash
pip install pandas
```

```python
import pandas as pd
```

### 2.2 Series
```python
# 1차원 데이터
s = pd.Series([1, 2, 3, 4, 5])

# 인덱스 지정
s = pd.Series([10, 20, 30], index=["a", "b", "c"])
print(s["a"])         # 10
print(s[0])           # 10 (위치)
```

### 2.3 DataFrame
```python
# dict 에서
data = {
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 35],
    "city": ["Seoul", "Busan", "Daegu"],
}
df = pd.DataFrame(data)

print(df)
#       name  age   city
# 0    Alice   25  Seoul
# 1      Bob   30  Busan
# 2  Charlie   35  Daegu
```

### 2.4 데이터 로드
```python
# CSV
df = pd.read_csv("data.csv")
df = pd.read_csv("data.csv", encoding="utf-8", index_col=0)

# Excel
df = pd.read_excel("data.xlsx", sheet_name="Sheet1")

# JSON
df = pd.read_json("data.json")

# DB
import sqlalchemy
engine = sqlalchemy.create_engine("sqlite:///data.db")
df = pd.read_sql("SELECT * FROM users", engine)

# URL 에서 직접
df = pd.read_csv("https://example.com/data.csv")
```

### 2.5 데이터 저장
```python
df.to_csv("output.csv", index=False, encoding="utf-8")
df.to_excel("output.xlsx", index=False)
df.to_json("output.json", orient="records", force_ascii=False)
df.to_sql("table_name", engine, if_exists="replace")
```

### 2.6 탐색
```python
df.head()              # 처음 5행
df.tail(10)            # 마지막 10행
df.sample(5)           # 무작위 5행
df.info()              # 정보 (dtype, null, ...)
df.describe()          # 통계 요약
df.shape               # (행, 열)
df.columns             # 열 이름
df.dtypes              # 타입
df.isna().sum()        # null 개수
df.duplicated().sum()  # 중복 행
```

### 2.7 선택
```python
# 열 선택
df["name"]             # Series
df[["name", "age"]]    # DataFrame

# 행 선택
df.iloc[0]             # 첫 행 (위치)
df.loc[0]              # 인덱스 0
df.iloc[0:3]           # 0-2행
df.loc[df["age"] > 25] # 조건 필터

# 셀
df.at[0, "name"]       # 정확한 위치 (빠름)
df.iloc[0, 1]          # 위치
```

### 2.8 필터링
```python
# 조건
adults = df[df["age"] >= 18]
seoul_adults = df[(df["age"] >= 18) & (df["city"] == "Seoul")]

# isin
df[df["city"].isin(["Seoul", "Busan"])]

# 문자열 메서드
df[df["name"].str.contains("A")]
df[df["name"].str.startswith("A")]
```

### 2.9 정렬
```python
# 단일 열
df.sort_values("age")
df.sort_values("age", ascending=False)

# 여러 열
df.sort_values(["city", "age"], ascending=[True, False])

# 인덱스
df.sort_index()
```

### 2.10 그룹화
```python
# 평균
df.groupby("city")["age"].mean()

# 여러 통계
df.groupby("city").agg({
    "age": ["mean", "max", "min"],
    "name": "count",
})

# 사용자 함수
df.groupby("city").agg(
    avg_age=("age", "mean"),
    count=("name", "count"),
)

# 여러 컬럼으로
df.groupby(["city", "gender"])["age"].mean()
```

### 2.11 결측치 처리
```python
df.isna()                          # bool DataFrame
df.isna().sum()                    # 열별 null 개수

# 제거
df.dropna()                        # null 있는 행 제거
df.dropna(subset=["name"])         # 특정 열만 검사

# 채우기
df.fillna(0)
df.fillna({"age": df["age"].mean(), "name": "Unknown"})

# 앞/뒤 값으로
df.fillna(method="ffill")          # 앞 값
df.fillna(method="bfill")          # 뒤 값
```

### 2.12 변형
```python
# 열 추가
df["age_group"] = df["age"].apply(lambda x: "성인" if x >= 18 else "미성년")

# 열 변환
df["age_squared"] = df["age"] ** 2
df["name_upper"] = df["name"].str.upper()

# 여러 열에서 새 열
df["full"] = df["name"] + " (" + df["city"] + ")"

# apply
df["greeting"] = df.apply(lambda row: f"Hi {row['name']} from {row['city']}", axis=1)

# 매핑
gender_map = {"M": "남성", "F": "여성"}
df["gender_kr"] = df["gender"].map(gender_map)

# 열 삭제
df = df.drop(columns=["temp_col"])

# 열 이름 변경
df = df.rename(columns={"name": "이름", "age": "나이"})
```

### 2.13 합치기
```python
# 행 추가 (위/아래)
combined = pd.concat([df1, df2], ignore_index=True)

# 열 추가 (좌/우)
combined = pd.concat([df1, df2], axis=1)

# 조인 (SQL JOIN)
merged = pd.merge(df1, df2, on="user_id")
merged = pd.merge(df1, df2, left_on="id", right_on="user_id", how="left")
# how: inner, outer, left, right
```

### 2.14 피벗 / 멜트
```python
# 와이드 → 롱
melted = df.melt(id_vars=["name"], value_vars=["math", "english"],
                 var_name="subject", value_name="score")

# 롱 → 와이드
pivot = melted.pivot(index="name", columns="subject", values="score")

# 피벗 테이블 (집계)
pt = df.pivot_table(
    values="sales",
    index="region",
    columns="month",
    aggfunc="sum",
    fill_value=0,
)
```

### 2.15 시계열
```python
# 날짜 파싱
df["date"] = pd.to_datetime(df["date"])
df.set_index("date", inplace=True)

# 리샘플링
df.resample("D").mean()       # 일 평균
df.resample("M").sum()        # 월 합계
df.resample("W").max()        # 주 최대

# 이동 평균
df["ma7"] = df["value"].rolling(7).mean()

# 차이/변화율
df["diff"] = df["value"].diff()
df["pct"] = df["value"].pct_change()

# 시프트 (lag)
df["lag1"] = df["value"].shift(1)
```

## 3. 시각화 (Matplotlib)

### 3.1 설치
```bash
pip install matplotlib seaborn
```

### 3.2 기본 플롯
```python
import matplotlib.pyplot as plt

# 라인 플롯
plt.figure(figsize=(10, 6))
plt.plot([1, 2, 3, 4], [10, 20, 25, 30], marker="o", label="Data")
plt.title("My Plot")
plt.xlabel("X axis")
plt.ylabel("Y axis")
plt.legend()
plt.grid(True)
plt.show()

# 또는 객체 지향 방식
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot([1, 2, 3], [10, 20, 30])
ax.set_title("Title")
ax.set_xlabel("X")
ax.set_ylabel("Y")
plt.show()
```

### 3.3 여러 종류의 차트
```python
import numpy as np

x = np.linspace(0, 10, 100)

# 산점도
plt.scatter(x, np.sin(x))

# 막대
plt.bar(["A", "B", "C"], [10, 20, 15])

# 히스토그램
plt.hist(np.random.randn(1000), bins=30)

# 박스플롯
plt.boxplot([np.random.randn(100), np.random.randn(100) + 2])

# 파이
plt.pie([30, 25, 20, 25], labels=["A", "B", "C", "D"], autopct="%1.1f%%")
```

### 3.4 서브플롯
```python
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

axes[0, 0].plot(x, np.sin(x))
axes[0, 0].set_title("Sin")

axes[0, 1].plot(x, np.cos(x))
axes[0, 1].set_title("Cos")

axes[1, 0].plot(x, np.tan(x))
axes[1, 0].set_title("Tan")
axes[1, 0].set_ylim(-5, 5)

axes[1, 1].scatter(np.random.randn(50), np.random.randn(50))
axes[1, 1].set_title("Scatter")

plt.tight_layout()
plt.savefig("plot.png", dpi=150)
plt.show()
```

### 3.5 DataFrame에서 직접 플롯
```python
df.plot(kind="line", x="date", y="sales", figsize=(10, 5))
df["age"].hist(bins=20)
df.groupby("city")["age"].mean().plot(kind="bar")
df.plot.scatter(x="x", y="y")
df.boxplot(column="value", by="group")
```

## 4. Seaborn (예쁜 통계 시각화)

```python
import seaborn as sns

# 분포
sns.histplot(df["age"], kde=True)
sns.kdeplot(df["age"])

# 카테고리
sns.barplot(data=df, x="city", y="age")
sns.boxplot(data=df, x="city", y="age")
sns.violinplot(data=df, x="city", y="age")

# 관계
sns.scatterplot(data=df, x="age", y="income", hue="city")
sns.lmplot(data=df, x="age", y="income")  # 회귀선 포함

# 히트맵 (상관관계)
sns.heatmap(df.corr(), annot=True, cmap="coolwarm")

# 페어플롯
sns.pairplot(df, hue="city")

# 스타일
sns.set_style("whitegrid")
sns.set_theme(palette="viridis")
```

## 5. 실전: 데이터 분석 파이프라인

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 로드
df = pd.read_csv("sales.csv")

# 2. 탐색
print(df.info())
print(df.describe())
print(df.head())

# 3. 정제
df["date"] = pd.to_datetime(df["date"])
df = df.dropna(subset=["amount"])
df["amount"] = df["amount"].astype(float)

# 4. 새 컬럼
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["weekday"] = df["date"].dt.day_name()

# 5. 분석
monthly = df.groupby([df["date"].dt.to_period("M")])["amount"].sum()
top_products = df.groupby("product")["amount"].sum().nlargest(10)
by_region = df.groupby("region").agg(
    total=("amount", "sum"),
    count=("id", "count"),
    avg=("amount", "mean"),
).round(2)

# 6. 시각화
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

monthly.plot(ax=axes[0, 0], title="월별 매출")
top_products.plot(kind="barh", ax=axes[0, 1], title="Top 10 제품")
by_region["total"].plot(kind="pie", ax=axes[1, 0], title="지역별 비율")
sns.heatmap(df.pivot_table(values="amount", index="region", columns="month", aggfunc="sum"),
            ax=axes[1, 1], cmap="YlOrRd")

plt.tight_layout()
plt.savefig("report.png", dpi=150)
```

## 6. Jupyter Notebook

데이터 분석에 최적의 환경.

```bash
pip install jupyter
jupyter notebook

# 또는 JupyterLab
pip install jupyterlab
jupyter lab
```

### 매직 명령
```ipython
%timeit sum(range(1000))
%matplotlib inline           # 인라인 그래프
%load_ext autoreload         # 자동 리로드
%autoreload 2

# 셸 명령
!pip install pandas
!ls -la
```

## 7. 더 빠른 대안

### 7.1 Polars (현대적, 빠름)
```bash
pip install polars
```

```python
import polars as pl

df = pl.read_csv("data.csv")
df.filter(pl.col("age") > 25).group_by("city").agg(pl.col("salary").mean())
```

### 7.2 DuckDB (SQL on dataframe)
```python
import duckdb

result = duckdb.query("SELECT city, AVG(age) FROM df GROUP BY city").df()
```

## 📝 연습 문제

### 문제 1: NumPy 배열
1부터 100까지의 정수로 10x10 배열을 만들고 짝수만 필터링하세요.

### 문제 2: DataFrame 생성
이름, 나이, 도시, 점수가 있는 5명의 학생 데이터프레임을 만드세요.

### 문제 3: CSV 분석
주어진 CSV 를 읽어 결측치를 처리하고 기본 통계를 출력하세요.

### 문제 4: 그룹화
판매 데이터에서 카테고리별, 월별 매출 합계를 구하세요.

### 문제 5: 시각화
DataFrame 의 컬럼 분포를 히스토그램과 박스플롯으로 그리세요.

## ✅ 체크리스트
- [ ] NumPy 배열을 생성하고 조작한다
- [ ] DataFrame 으로 데이터를 다룬다
- [ ] CSV/Excel/JSON 을 읽고 쓴다
- [ ] groupby, merge, pivot 을 활용한다
- [ ] 결측치를 처리한다
- [ ] Matplotlib/Seaborn 으로 시각화한다

## 🔗 다음 챕터
👉 [04. 자동화 스크립트](./04-automation.md)
