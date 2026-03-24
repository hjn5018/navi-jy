import os
import sys
import subprocess
import shutil

def check_command(cmd: str) -> bool:
    """Checks if a command exists in the system PATH."""
    return shutil.which(cmd) is not None

def get_status_emoji(satisfied: bool) -> str:
    return "✅ OK" if satisfied else "❌ MISSING"

def run_environment_check():
    """Diagnostic script to check for development/deployment prerequisites."""
    print("="*50)
    print("      NAVI Environment Health Check      ")
    print("="*50)
    
    python_ok = sys.version_info >= (3, 10)
    node_ok = check_command("node")
    npm_ok = check_command("npm")
    ffmpeg_ok = check_command("ffmpeg")
    
    print(f"1. Python 3.10+ : {get_status_emoji(python_ok)} (Current: {sys.version})")
    print(f"2. Node.js      : {get_status_emoji(node_ok)}")
    print(f"3. NPM          : {get_status_emoji(npm_ok)}")
    print(f"4. FFmpeg (Audio): {get_status_emoji(ffmpeg_ok)} (Required for high-quality audio processing)")
    
    print("-" * 50)
    
    if all([python_ok, node_ok, npm_ok]):
        print("[!] 모든 핵심 요구 사항이 충족되었습니다. NAVI를 실행할 준비가 되었습니다.")
    else:
        print("[!] 주의: 일부 요구 사항이 누락되었습니다. 'setup_guide.md'를 참조하여 설치를 완료해주세요.")
        if not ffmpeg_ok:
            print("[Tip] FFmpeg는 음성 처리를 위해 권장됩니다. (Chocolatey 등으로 설치 가능)")
            
    print("\n" + "="*50)
    input("결과 확인 후 아무 키나 누르면 종료됩니다... (Press Enter to exit)")

if __name__ == "__main__":
    run_environment_check()
