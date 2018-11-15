##좌표 변환 python

[국토 지리원 좌표변환 지침](http://www.ngii.go.kr/kor/board/view.do?rbsIdx=31&idx=251)을 참고하여 작성된 좌표 변환 프로그램

#### 실행 방법

```python
# TM -> 경위도
TM_to_LatLong(X, Y)

# 경위도 -> TM
LatLong_to_TM(latitude, longtitude)
```

#### 실행 옵션

함수 인자에 추가로 아래의 parameter 값을 지정하여 실행

- `origin`
  - `midOrigin` : 중부원점 (default)
  - `westOrigin` : 서부원점
  - `eastOrigin` : 동부원점
  - `eastSeaOrigin` : 동해원점
- `ellipsoid`
  - `grs80` : GRS80 타원체 (default)
  - `bessel` : Bessel 타원체