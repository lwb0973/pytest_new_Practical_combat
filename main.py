import os
import shutil
import subprocess
import time
import settings


def clean_old_results():
    print("🧹 清理旧的测试结果...")
    if os.path.exists(settings.RESULT_FILE):
        shutil.rmtree(settings.RESULT_FILE)
    os.makedirs(settings.RESULT_FILE, exist_ok=True)

def run_pytest():
    print("🚀 正在运行测试用例...")
    result = pytest.main(['-s', '-v', f'--alluredir={settings.RESULT_FILE}', settings.TEST_PATH])
    if result != 0:
        print("❗ 有测试用例失败，请检查！")
    return result


def generate_report():
    print("📊 正在生成 Allure 报告...")
    try:
        subprocess.run([settings.ALLURE_COMMAND, 'generate', settings.RESULT_FILE, '-o', settings.REPORT_DIR, '--clean'], check=True)

    except FileNotFoundError:

        print("❌ 未找到 allure 命令，请检查是否配置到环境变量！")
        exit(1)
    print("✅ 报告生成成功！")

def open_report():
    print("🌐 正在打开测试报告...")
    try:
        subprocess.Popen([settings.ALLURE_COMMAND, 'open', settings.REPORT_DIR], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # 可选：直接在浏览器打开固定端口，例如 http://localhost:1234
        # webbrowser.open("http://localhost:1234")
    except Exception as e:
        print(f"❌ 打开报告失败：{e}")

if __name__ == '__main__':
    try:
        import pytest
    except ImportError:
        print("❌ 没有安装 pytest，请先运行 pip install pytest")
        exit(1)

    clean_old_results()
    run_pytest()
    time.sleep(1)
    generate_report()
    open_report()
