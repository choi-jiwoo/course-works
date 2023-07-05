# 국민 청원 게시글 데이터를 활용한 감성 분석

## 분석 보고서

보고서 내용은 [rpubs](https://rpubs.com/cho2jiwoo/802248)에서 확인해 보실 수 있습니다.

## 데이터

청원 게시글 데이터와 텍스트 분석시 사용된 데이터들을 압축해 놓았습니다.

| [data.zip](https://github.com/choi-jiwoo/course-works/tree/master/course/ajou_university/statistical_data_analysis_using_R/midterm_project/data)

### 2019/4/30~2021/1/20 국민 청원 게시글

| `petition_data.csv`

| Header        | Definition    |
| :------------ | ------------- |
| `id`          | 청원 번호       |
| `category`    | 청원 분류       |
| `title`       | 청원 제목       |
| `expiryDate`  | 청원 만료일      |
| `numOfAgrees` | 청원 참여인원    |

출처 : https://www1.president.go.kr/petitions

### 텍스트 분석시 사용한 파일

- `한국불용어100.txt`
- `customDic.txt`
- `del.txt`
- `negative.txt`
- `positive.txt`
