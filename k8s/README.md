# Kubernetes

이 디렉터리는 Swelling FastAPI MSA 서버를 Kubernetes에 배포하기 위한 기본 환경입니다.

## 구성

```text
k8s/
  base/
    namespace.yaml
    configmap.yaml
    service-account.yaml
    gateway.yaml
    users.yaml
    swelling.yaml
    notifications.yaml
    kustomization.yaml
  overlays/
    local/
      kustomization.yaml
```

각 Deployment는 같은 컨테이너 이미지를 사용하고, `SERVICE_MODULE`과 `PORT` 환경변수로 실행할 FastAPI 앱을 선택합니다.

## 로컬 적용

```bash
cd ~/Desktop/Swelling_FastAPIServer
docker build -t swelling-fastapi-server:local .
kubectl apply -k k8s/overlays/local
kubectl get all -n swelling
kubectl port-forward -n swelling svc/gateway 8000:8000
```

kind를 사용한다면 apply 전에 이미지를 로드합니다.

```bash
kind load docker-image swelling-fastapi-server:local
```

minikube를 사용한다면 다음을 실행합니다.

```bash
minikube image load swelling-fastapi-server:local
```

삭제:

```bash
kubectl delete -k k8s/overlays/local
```

## 운영 배포 시 변경할 부분

- `k8s/overlays/local/kustomization.yaml`의 이미지 이름/태그를 실제 레지스트리 이미지로 변경
- ConfigMap의 내부 서비스 URL이 클러스터 DNS와 맞는지 확인
- Ingress, TLS, HPA, Secret, DB 연결 정보 추가
