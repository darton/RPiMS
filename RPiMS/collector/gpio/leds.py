from gpiozero import LED

def init_led_indicators(ctx):
    leds = {}
    for name, cfg in ctx.gpio.items():
        if cfg['type'] == 'door_led':
            leds['door_led'] = LED(cfg['pin'])
        elif cfg['type'] == 'motion_led':
            leds['motion_led'] = LED(cfg['pin'])
        elif cfg['type'] == 'led':
            leds['led'] = LED(cfg['pin'])
    return leds

