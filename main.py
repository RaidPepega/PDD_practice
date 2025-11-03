import traceback
import os
from kivy.app import App
from kivy.uix.label import Label

try:
    # Запишем что Python стартовал
    with open('/storage/emulated/0/Download/start.txt', 'w') as f:
        f.write("Python запустился!")


    class TestApp(App):
        def build(self):
            return Label(text='Тест!')


    TestApp().run()

except Exception as e:
    # Запишем ошибку
    with open('/storage/emulated/0/Download/error.txt', 'w') as f:
        f.write(f"ОШИБКА: {str(e)}\n")
        f.write(traceback.format_exc())