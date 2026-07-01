# Agent.md

## 프로젝트 개요
- 목적: 실시간 맞춤법 교정 AI 모바일 앱
- 언어 : Python 3.14
- 프레임 워크 : FastAPI
  
  
## 디렉토리 구조
```
.
├── services/                  # FastAPI 마이크로서비스
│   ├── gateway/               # API Gateway
│   │   └── app/
│   ├── users/                 # 사용자 서비스
│   │   └── app/
│   ├── swelling/              # 부종 리포트 서비스
│   │   └── app/
│   └── notifications/         # 알림 서비스
│       └── app/
├── src/
│   └── swelling_common/       # 공통 설정 및 헬스체크 유틸
├── scripts/                   # 로컬 실행 스크립트
├── tests/                     # 테스트 코드
├── k8s/                       # Kubernetes 매니페스트
│   ├── base/
│   └── overlays/
│       └── local/
├── .github/                   # GitHub 이슈/PR 템플릿 및 워크플로우
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── pyproject.toml
└── README.md
```

## 코드 규칙
- 함수명: snake_case
- 클래스명: PascalCase
- 한 함수는 하나의 역할만 수행한다
- 타입 힌트 필수

## 절대 금지
- 타 LLM/자동화 에이전트는 `AGENTS.md`를 절대 수정하지 않는다. 수정은 저장소 소유자의 명시적인 직접 요청이 있을 때만 가능하다.
- `src/core/` 파일 수정 금지 (레거시, 건드리면 장애 발생)
- `print()` 사용 금지 → `logger.info()` 사용
- 직접 DB 쿼리 금지 → 반드시 서비스 레이어 경유

## PR 규칙
- PR 하나에 하나의 변경만
- 테스트 없는 PR은 올리지 않는다

## Commit Convention
- 커밋 메시지: conventional commit
- 사용 언어: 한국어
- 형식:
  <타입>[적용 범위]: <1줄 설명>

## Test
- 테스트 파일 위치 : `tests/` 디렉토리
- 실행 명령 : `pytest tests/`
- 새 기능에는 반드시 테스트 추가
