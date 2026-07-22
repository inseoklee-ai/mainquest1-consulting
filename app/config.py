"""환경설정 로드 (design add-supabase-auth D4).

.env 파일에서 비밀값을 읽는다. 저장소에는 커밋하지 않는다(.gitignore).
로컬: 프로젝트 루트의 .env
배포(Render): 대시보드 환경변수
"""
import os

from dotenv import load_dotenv

load_dotenv()  # 루트의 .env를 환경변수로 로드 (없으면 무시)

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")
# 세션 쿠키 서명용. 없으면 개발용 임시값(배포 시 반드시 설정).
SESSION_SECRET = os.getenv("SESSION_SECRET", "dev-only-insecure-secret-change-me")

# 인증 기능 활성화 여부: 키가 모두 있을 때만 로그인 기능을 켠다.
AUTH_ENABLED = bool(SUPABASE_URL and SUPABASE_ANON_KEY)
