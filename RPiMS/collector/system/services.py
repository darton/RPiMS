import subprocess

def av_stream(state):
    _cmd = f'sudo systemctl {state} mediamtx.service'
    subprocess.Popen(_cmd, shell=True)


def hostnamectl_sh(**kwargs):
    hctldict = {
        "location": "set-location",
        "chassis": "set-chassis",
        "deployment": "set-deployment",
    }

    # set hostname
    hostname = kwargs.get('hostname')
    if hostname:
        subprocess.Popen([
            'sudo', 'raspi-config', 'nonint', 'do_hostname', hostname
        ])

    # use hostnamectl
    for key, action in hctldict.items():
        value = kwargs.get(key)
        if value:
            subprocess.Popen([
                'sudo', '/usr/bin/hostnamectl', action, value
            ])


def get_hostip():
    _cmd = 'sudo ../scripts/gethostinfo.sh'
    subprocess.Popen(_cmd, shell=True)
