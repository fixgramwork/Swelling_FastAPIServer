from __future__ import annotations

import os
import signal
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Service:
    name: str
    module: str
    port: int


SERVICES = [
    Service("users", "services.users.app.main:app", 8001),
    Service("swelling", "services.swelling.app.main:app", 8002),
    Service("notifications", "services.notifications.app.main:app", 8003),
    Service("gateway", "services.gateway.app.main:app", 8000),
]


def build_env() -> dict[str, str]:
    env = os.environ.copy()
    pythonpath = [str(ROOT_DIR / "src"), str(ROOT_DIR)]
    if env.get("PYTHONPATH"):
        pythonpath.append(env["PYTHONPATH"])
    env["PYTHONPATH"] = os.pathsep.join(pythonpath)
    env.setdefault("USERS_SERVICE_URL", "http://127.0.0.1:8001")
    env.setdefault("SWELLING_SERVICE_URL", "http://127.0.0.1:8002")
    env.setdefault("NOTIFICATIONS_SERVICE_URL", "http://127.0.0.1:8003")
    return env


def start_service(service: Service, env: dict[str, str]) -> subprocess.Popen[bytes]:
    print(f"starting {service.name} on http://127.0.0.1:{service.port}", flush=True)
    return subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            service.module,
            "--host",
            "127.0.0.1",
            "--port",
            str(service.port),
            "--reload",
            "--reload-dir",
            str(ROOT_DIR / "services"),
            "--reload-dir",
            str(ROOT_DIR / "src"),
        ],
        cwd=ROOT_DIR,
        env=env,
    )


def main() -> int:
    env = build_env()
    processes = [start_service(service, env) for service in SERVICES]

    def stop_all(_signum: int | None = None, _frame: object | None = None) -> None:
        for process in processes:
            if process.poll() is None:
                process.terminate()
        for process in processes:
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()

    signal.signal(signal.SIGINT, stop_all)
    signal.signal(signal.SIGTERM, stop_all)

    try:
        while True:
            for process in processes:
                if process.poll() is not None:
                    stop_all()
                    return process.returncode or 1
            signal.pause()
    finally:
        stop_all()


if __name__ == "__main__":
    raise SystemExit(main())
