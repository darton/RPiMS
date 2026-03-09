import logging
import subprocess
import socket


logger = logging.getLogger(__name__)


def shutdown():
    subprocess.check_call(['sudo', 'poweroff'])


def get_hostip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "0.0.0.0"


def old_zabbix_sender_call(message, sensor_id):
    _cmd = f'/opt/RPiMS/scripts/zabbix_sender.sh {message} {str(sensor_id)}'
    subprocess.Popen([_cmd],shell=True)


def zabbix_sender_call(ctx, key, value):
    if not ctx.config.get('use_zabbix_sender'):
        return

    try:
        subprocess.check_call([
            'zabbix_sender',
            '-c', '/opt/RPiMS/config/zabbix_rpims.conf',
            '-s', ctx.zabbix_agent.get('hostname'),
            '-k', key,
            '-o', str(value),
            ],)
    except Exception as e:
        logger.error(f"Zabbix sender error: {e}")


def mediamtx_keepalive(ctx, timeout=10):
    try:
        subprocess.Popen([
            "systemd-run",
            "--unit=mediamtx-keepalive",
            "--scope",
            f"--property=RuntimeMaxSec={timeout}",
            "systemctl", "start", "mediamtx-keepalive.service"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        logger.error(f"Failed to trigger MediaMTX keepalive: {e}")
