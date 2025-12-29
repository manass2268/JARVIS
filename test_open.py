# test_open.py
import Backend.command as cmd
# disable speak to avoid Eel dependency during test
cmd.speak = lambda text: None

from Backend import feature
feature.openCommand('open notepad')