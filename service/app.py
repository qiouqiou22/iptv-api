import os
import sys

sys.path.append(os.path.dirname(sys.path[0]))
from flask import Flask, send_from_directory, make_response
from utils.tools import get_result_file_content, get_ip_address, resource_path, get_grouped_result_path
from utils.config import config
import utils.constants as constants

app = Flask(__name__)


@app.route("/")
def show_index():
    return get_result_file_content()


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(resource_path('static/images'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@app.route("/txt")
def show_txt():
    return get_result_file_content(file_type="txt")


@app.route("/m3u")
def show_m3u():
    return get_result_file_content(file_type="m3u")


@app.route("/content")
def show_content():
    return get_result_file_content(show_content=True)


@app.route("/main")
def show_main():
    return get_result_file_content(result_file=get_grouped_result_path("main"))


@app.route("/main.txt")
def show_main_txt():
    return get_result_file_content(file_type="txt", result_file=get_grouped_result_path("main"))


@app.route("/main.m3u")
def show_main_m3u():
    return get_result_file_content(file_type="m3u", result_file=get_grouped_result_path("main"))


@app.route("/backup")
def show_backup():
    return get_result_file_content(result_file=get_grouped_result_path("backup"))


@app.route("/backup.txt")
def show_backup_txt():
    return get_result_file_content(file_type="txt", result_file=get_grouped_result_path("backup"))


@app.route("/backup.m3u")
def show_backup_m3u():
    return get_result_file_content(file_type="m3u", result_file=get_grouped_result_path("backup"))


@app.route("/log")
def show_log():
    log_path = resource_path(constants.sort_log_path)
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as file:
            content = file.read()
    else:
        content = constants.waiting_tip
    response = make_response(content)
    response.mimetype = "text/plain"
    return response


def run_service():
    try:
        if not os.environ.get("GITHUB_ACTIONS"):
            ip_address = get_ip_address()
            print(f"📄 Result content: {ip_address}/content")
            print(f"📄 Log content: {ip_address}/log")
            print(f"🚀 M3u api: {ip_address}/m3u")
            print(f"🚀 Txt api: {ip_address}/txt")
            print(f"🚀 Main m3u api: {ip_address}/main.m3u")
            print(f"🚀 Main txt api: {ip_address}/main.txt")
            print(f"🚀 Backup m3u api: {ip_address}/backup.m3u")
            print(f"🚀 Backup txt api: {ip_address}/backup.txt")
            print(f"✅ You can use this url to watch IPTV 📺: {ip_address}")
            app.run(host="0.0.0.0", port=config.app_port)
    except Exception as e:
        print(f"❌ Service start failed: {e}")


if __name__ == "__main__":
    run_service()
