# Swelling FastAPI Server

FastAPI 기반 MSA 백엔드 서버 템플릿입니다. 하나의 GitHub 저장소 안에서 API Gateway와 도메인별 서비스를 분리해 로컬 또는 Docker Compose로 실행할 수 있습니다.

## 구조

```text
services/
  gateway/          # 외부 진입점, 내부 서비스 라우팅
  users/            # 사용자 서비스
  swelling/         # 부종 리포트 서비스
  notifications/    # 알림 서비스
src/swelling_common # 공통 설정/헬스체크 유틸
scripts/            # 로컬 멀티 서비스 실행 스크립트
tests/              # 기본 헬스체크 테스트
```

## 로컬 실행

```bash
cd ~/Desktop/Swelling_FastAPIServer
make install
make dev
```

실행 후 다음 URL을 사용할 수 있습니다.

- API 문서: http://127.0.0.1:8000/docs
- Gateway Health: http://127.0.0.1:8000/health
- Users Service: http://127.0.0.1:8001/docs
- Swelling Service: http://127.0.0.1:8002/docs
- Notifications Service: http://127.0.0.1:8003/docs

## Docker Compose 실행

```bash
cd ~/Desktop/Swelling_FastAPIServer
docker compose up --build
```

## 예시 요청

```bash
curl -X POST http://127.0.0.1:8000/api/v1/users/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Kim Minjae","email":"minjae@example.com"}'

curl -X POST http://127.0.0.1:8000/api/v1/swelling/reports \
  -H "Content-Type: application/json" \
  -d '{"user_id":"USER_ID","body_part":"ankle","severity":3,"memo":"after running"}'
```

## 테스트

```bash
make test
```

## GitHub 연결

이 폴더는 다음 원격 저장소와 연결되어 있습니다.

```bash
origin https://github.com/fixgramwork/Swelling_FastAPIServer.git
```

초기 커밋 후 푸시:

```bash
git add .
git commit -m "Initialize FastAPI MSA backend"
git push -u origin main
```
