from gpiozero import Button
from system.actions import shutdown


def init_system_buttons(ctx):
    buttons = {}
    if ctx.config.get('use_system_buttons'):
        for name, cfg in ctx.gpio.items():
            if cfg['type'] == 'ShutdownButton':
                buttons['shutdown_button'] = Button(cfg['pin'], hold_time=int(cfg['hold_time']))
    return buttons

def setup_system_buttons_callbacks(ctx):
    if ctx.config.get('use_system_buttons'):
        ctx.system_buttons['shutdown_button'].when_held = shutdown
