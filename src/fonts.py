import pyglet

def get_monospaced_font():
    pyglet.font.add_file('fonts/FiraMono-Regular.ttf') # change the location when compiling
    return 'Fira Mono'

def get_regular_font():
    pyglet.font.add_file('fonts/FiraSans-Regular.ttf')
    return 'Fira Sans'
