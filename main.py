from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.uix.popup import Popup
from kivy.logger import Logger
import random
import json
import os
from kivy.utils import platform
import traceback

try:
    # Проверка какие файлы есть в APK
    import os

    files = os.listdir('.')
    with open('/storage/emulated/0/Download/apk_files.txt', 'w') as f:
        f.write("Файлы в APK:\n")
        for file in files:
            f.write(f"{file}\n")

        # Проверка папки data
        if os.path.exists('data'):
            data_files = os.listdir('data')
            f.write("\nФайлы в data/:\n")
            for file in data_files[:10]:  # первые 10 файлов
                f.write(f"{file}\n")

    # Умная запись отладки для Android и ПК
    debug_dir = '/storage/emulated/0/Download' if os.path.exists('/storage/emulated/0/Download') else '.'
    start_file = os.path.join(debug_dir, 'debug_start.txt')

    with open(start_file, 'w') as f:
        f.write("Основное приложение запускается...")

    class MenuScreen(Screen):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

            layout = BoxLayout(orientation='vertical', padding=30, spacing=15)

            title_label = Label(
                text='ПДД ПРАКТИКА',
                font_size='40sp',
                size_hint=(1, 0.3)
            )
            layout.add_widget(title_label)

            subtitle_label = Label(
                text='Выберите режим игры',
                font_size='24sp',
                size_hint=(1, 0.1)
            )
            layout.add_widget(subtitle_label)

            #20 вопросов подряд"
            all_quiz_btn = Button(
                text='Тянуть билет',
                font_size='20sp',
                size_hint=(0.9, 0.2),
                pos_hint={'center_x': 0.5},
                background_color=(0.35, 0.65, 0.35, 1),
                background_normal='',
                background_down=''
            )
            all_quiz_btn.bind(on_press=self.start_all_quiz)
            layout.add_widget(all_quiz_btn)

            # "Выбор темы" для целенаправленной тренировки
            themes_btn = Button(
                text='Выбор темы',
                font_size='20sp',
                size_hint=(0.9, 0.2),
                pos_hint={'center_x': 0.5},
                background_color=(0.9, 0.85, 0.25, 1),
                background_normal = '',
                background_down = ''
            )
            themes_btn.bind(on_press=self.show_themes)
            layout.add_widget(themes_btn)

            # Кнопка выхода
            exit_btn = Button(
                text='Выход',
                font_size='18sp',
                size_hint=(0.9, 0.2),
                pos_hint={'center_x': 0.5},
                background_color=(1, 0.3, 0.3, 1)
            )
            exit_btn.bind(on_press=self.exit_app)
            layout.add_widget(exit_btn)

            self.add_widget(layout)

        def start_all_quiz(self, instance):
            # квиз с 20 случайными вопросами из разных тем
            app = App.get_running_app()

            if len(app.all_questions) >= 20:
                random_questions = random.sample(app.all_questions, 20)
            else:
                random_questions = app.all_questions

            print(f"🎯 Запуск квиза: {len(random_questions)} случайных вопросов")

            app.start_quiz(random_questions, "20 случайных вопросов")

        def show_themes(self, instance):
            # экран с темами
            app = App.get_running_app()
            app.screen_manager.current = 'themes'

        def exit_app(self, instance):
            #закрыть приложуху
            App.get_running_app().stop()


    class ThemesScreen(Screen):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

            from kivy.uix.floatlayout import FloatLayout

            layout = FloatLayout()

            title_label = Label(
                text='Выберите тему',
                font_size='32sp',
                size_hint=(1, 0.1),
                pos_hint={'center_x': 0.5, 'top': 0.95}
            )
            layout.add_widget(title_label)

            from kivy.uix.scrollview import ScrollView

            # список с перемоткой
            scroll_view = ScrollView(
                size_hint=(0.8, 0.7),
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )

            self.themes_layout = BoxLayout(
                orientation='vertical',
                spacing=8,
                size_hint_y=None,
                size_hint_x=1,
                pos_hint={'center_x': 0.5},
                padding=[0, 0]
            )
            self.themes_layout.bind(minimum_height=self.themes_layout.setter('height'))

            scroll_view.add_widget(self.themes_layout)
            layout.add_widget(scroll_view)

            back_btn = Button(
                text='← Назад в меню',
                font_size='16sp',
                size_hint=(0.7, 0.08),
                pos_hint={'center_x': 0.5, 'y': 0.02},
                background_color=(0.7, 0.7, 0.7, 1)
            )
            back_btn.bind(on_press=self.go_back)
            layout.add_widget(back_btn)

            self.add_widget(layout)
        def on_enter(self):
            self.update_themes_display()

        def update_themes_display(self):
            self.themes_layout.clear_widgets()
            app = App.get_running_app()

            # Создаем кнопку для каждой темы с отображением прогресса
            for theme_name, theme_data in app.themes.items():
                # Получение прогресса по этой теме
                progress = app.get_theme_progress(theme_name)
                total_questions = len(theme_data['questions'])

                # для прикола ахахаха
                if progress['best_score'] == total_questions:
                    emoji = ':)'
                    color = (0, 1, 0, 1)
                elif progress['best_score'] > 0:
                    emoji = ':|'
                    color = (0.9, 0.85, 0.25, 1)
                else:
                    emoji = ':('
                    color = (0.8, 0.8, 0.8, 1)

                button_text = f'{emoji} {theme_name}\n{progress["best_score"]}/{total_questions}'

                theme_btn = Button(
                    text=button_text,
                    font_size='14sp',
                    size_hint_y=None,
                    height=60,
                    background_color=color
                )
                theme_btn.bind(on_press=lambda instance, theme=theme_name: self.start_theme_quiz(theme))
                self.themes_layout.add_widget(theme_btn)

        def start_theme_quiz(self, theme_name):
            # квиз с выбранной темой
            app = App.get_running_app()
            theme_questions = app.themes[theme_name]['questions']
            app.start_quiz(theme_questions, theme_name)

        def go_back(self, instance):
            #главное меню
            app = App.get_running_app()
            app.screen_manager.current = 'menu'


    class QuizScreen(Screen):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
            self.add_widget(self.layout)

            self.current_theme_name = ""
            self.timer_active = False
            self.time_left = 0

        def cleanup_popups(self):
            #чтобы убрать все вылезающие меню, таблички и тд
            from kivy.app import App
            app = App.get_running_app()

            for child in app.root_window.children[:]:
                if hasattr(child, 'dismiss') and callable(child.dismiss):
                    try:
                        child.dismiss()
                    except:
                        pass

        def setup_quiz(self, questions, title):
            self.questions = questions
            self.quiz_title = title
            self.current_theme_name = title
            self.current_question = 0
            self.score = 0

            self.layout.clear_widgets()

            is_timed_quiz = "20 случайных вопросов" in title

            if is_timed_quiz:
                # вопросы на время
                top_panel = BoxLayout(orientation='horizontal', size_hint=(1, 0.12))

                #тема слева
                self.title_label = Label(
                    text=title,
                    font_size='14sp',
                    size_hint=(0.3, 1),
                    halign='left',
                    valign='top',
                    text_size=(None, None),
                    padding=(5, 5),
                    shorten=False
                )
                top_panel.add_widget(self.title_label)

                # Таймер по центру
                self.timer_label = Label(
                    text="20:00",
                    font_size='18sp',
                    size_hint=(0.4, 1),
                    halign='center',
                    valign='middle',
                    color=(0.9, 0.1, 0.1, 1),
                    bold=True
                )
                top_panel.add_widget(self.timer_label)

                # Счет справа
                self.score_label = Label(
                    text=f'Счет: {self.score}/{len(questions)}',
                    font_size='14sp',
                    size_hint=(0.3, 1),
                    halign='right',
                    valign='middle'
                )
                top_panel.add_widget(self.score_label)

                self.layout.add_widget(top_panel)

                # перенос текста при нехватке места
                def update_title_text_size(instance, value):
                    available_width = max(self.title_label.width - 10, 50)
                    self.title_label.text_size = (available_width, None)

                self.title_label.bind(width=update_title_text_size)
                update_title_text_size(self.title_label, None)

                self.start_timer(20 * 60)

            else:
                # для вопросов по определенным темам таймер не нужен
                # Заголовок по центру
                self.title_label = Label(
                    text=title,
                    font_size='18sp',
                    size_hint=(1, 0.08),
                    halign='center',
                    valign='middle',
                    bold=True,
                    text_size=(None, None),
                    padding=(10, 5),
                    shorten=False
                )
                self.layout.add_widget(self.title_label)

                def update_center_title_size(instance, value):
                    available_width = max(self.title_label.width - 20, 100)
                    self.title_label.text_size = (available_width, None)

                self.title_label.bind(width=update_center_title_size)
                update_center_title_size(self.title_label, None)

                # Счет по центру, под заголовком
                self.score_label = Label(
                    text=f'Счет: {self.score}/{len(questions)}',
                    font_size='16sp',
                    size_hint=(1, 0.04),
                    halign='center',
                    valign='middle'
                )
                self.layout.add_widget(self.score_label)

            # Картинка вопроса
            self.question_image = Image(
                size_hint=(1, 0.25),
                allow_stretch=True,
                keep_ratio=True
            )
            self.layout.add_widget(self.question_image)

            # сам вопрос
            self.question_label = Label(
                font_size='16sp',
                size_hint=(1, 0.15),
                text_size=(self.layout.width - 40, None),
                halign='center',
                valign='middle',
                padding=(10, 10)
            )
            self.layout.add_widget(self.question_label)

            def update_question_text_size(instance, value):
                self.question_label.text_size = (self.layout.width - 40, None)

            self.layout.bind(width=update_question_text_size)

            # Контейнер для кнопок
            self.answers_layout = BoxLayout(
                orientation='vertical',
                spacing=10,
                size_hint=(1, 0.5)
            )
            self.layout.add_widget(self.answers_layout)

            self.load_question()

        def start_timer(self, total_seconds):
            #таймер
            self.timer_active = True
            self.time_left = total_seconds
            self.update_timer_display()

            from kivy.clock import Clock
            self.timer_event = Clock.schedule_interval(self.update_timer, 1)

        def update_timer(self, dt):
            if not self.timer_active:
                return

            self.time_left -= 1
            self.update_timer_display()

            # закончилось время-конец
            if self.time_left <= 0:
                self.timer_active = False
                self.timer_event.cancel()
                self.time_up_finish_quiz()

        def update_timer_display(self):
            minutes = self.time_left // 60
            seconds = self.time_left % 60
            self.timer_label.text = f"{minutes:02d}:{seconds:02d}"

            # радужный таймер
            if self.time_left <= 60:
                self.timer_label.color = (1, 0, 0, 1)
            elif self.time_left <= 300:
                self.timer_label.color = (1, 0.5, 0, 1)
            else:
                self.timer_label.color = (0.1, 0.4, 0.8, 1)

        def time_up_finish_quiz(self):
            print("⏰ Время вышло! Завершаем квиз...")

            if hasattr(self, 'timer_event'):
                self.timer_event.cancel()

            # отключение кнопок чтобы не баловались
            if hasattr(self, 'answers_layout'):
                for button in self.answers_layout.children:
                    button.disabled = True

            self.show_time_up_message()

        def show_time_up_message(self):
            from kivy.uix.floatlayout import FloatLayout
            from kivy.clock import Clock

            time_up_layout = FloatLayout()

            with time_up_layout.canvas.before:
                Color(0.9, 0.1, 0.1, 0.9)  # Красный полупрозрачный
                Rectangle(pos=time_up_layout.pos, size=time_up_layout.size)

            message_label = Label(
                text="ВРЕМЯ ВЫШЛО! \nКвиз завершен",
                font_size='24sp',
                size_hint=(0.8, 0.4),
                pos_hint={'center_x': 0.5, 'center_y': 0.6},
                halign='center',
                color=(1, 1, 1, 1),
                bold=True
            )
            time_up_layout.add_widget(message_label)

            self.layout.add_widget(time_up_layout)

            # через 2 секунды как законилось время показываем результат
            Clock.schedule_once(lambda dt: self.show_final_results(), 2)

        def load_question(self):
            if self.current_question < len(self.questions):
                question_data = self.questions[self.current_question]
                app = App.get_running_app()

                if question_data['image'].startswith('http'):
                    self.question_image.source = question_data['image']
                    print(f"Загрузка картинки: {question_data['image']}")
                elif question_data['image']:
                    image_path = app.get_image_path(question_data['image'], self.get_current_theme_folder())
                    self.question_image.source = image_path
                    print(f"Загрузка картинки: {image_path}")
                else:
                    #заглушка если не было картинки
                    no_image_path = app.get_no_image_path()
                    self.question_image.source = no_image_path
                    print(f"Используем заглушку: {no_image_path}")

                question_text = question_data['question']

                # Только для очень длинных вопросов (>150 символов)
                if len(question_text) > 150:
                    self.question_label.font_size = '14sp'
                else:
                    self.question_label.font_size = '16sp'

                self.question_label.text = f'Вопрос {self.current_question + 1}: {question_text}'

                self.score_label.text = f'Счет: {self.score}/{len(self.questions)}'
                self.answers_layout.clear_widgets()

                shuffled_answers = question_data['answers'].copy()
                random.shuffle(shuffled_answers)

                #кнопки ответов
                for answer_text in shuffled_answers:
                    # Только для очень длинных ответов (>80 символов)
                    if len(answer_text) > 80:
                        font_size = '12sp'
                    elif len(answer_text) > 50:
                        font_size = '13sp'
                    else:
                        font_size = '14sp'

                    btn = Button(
                        text=answer_text,
                        font_size=font_size,
                        size_hint=(1, 0.2),
                        text_size=(self.answers_layout.width - 20, None),
                        halign='center',
                        valign='middle',
                        padding=(15, 5),
                        background_color=(0.2, 0.6, 1, 1),
                        background_normal='',
                        background_down='',
                        color=(1, 1, 1, 1)
                    )

                    def update_button_text_size(btn_instance, value):
                        btn_instance.text_size = (btn_instance.width - 20, None)

                    btn.bind(width=update_button_text_size)
                    btn.bind(on_press=lambda instance, ans=answer_text: self.check_answer(ans))
                    self.answers_layout.add_widget(btn)

                print(f"Загружен вопрос {self.current_question + 1}")
            else:
                print("Вопросы закончились, показываем результаты")
                self.show_final_results()
        def get_current_theme_folder(self):
            app = App.get_running_app()

            if "20 случайных вопросов" in self.current_theme_name and self.questions:
                current_question = self.questions[self.current_question]

                for theme_name, theme_data in app.themes.items():
                    if current_question in theme_data['questions']:
                        folder = theme_data['folder']
                        print(f"Вопрос из темы '{theme_name}', папка: '{folder}'")
                        return folder

                print("Не найдена тема для вопроса, используем папку по умолчанию")
                return 'images'

            elif self.current_theme_name in app.themes:
                folder = app.themes[self.current_theme_name]['folder']
                print(f"Обычная тема '{self.current_theme_name}', папка: '{folder}'")
                return folder

            print("нету темы, используем папку по умолчанию")
            return 'images'

        def use_no_image(self):
            app = App.get_running_app()
            no_image_path = app.get_no_image_path()
            self.question_image.source = no_image_path

        def check_answer(self, selected_answer):
            self.cleanup_popups()

            question_data = self.questions[self.current_question]
            correct_answer = question_data['correct_answer']

            answer_buttons = self.answers_layout.children[:]

            #подсвечивание кнопок
            for button in answer_buttons:
                if button.text == correct_answer:
                    # Правильный ответ - ЗЕЛЕНЫЙ (чуть темнее)
                    button.background_color = (0, 0.6, 0, 1)
                    button.background_disabled_normal = ''
                    button.disabled_color = (1, 1, 1, 1)
                elif button.text == selected_answer and selected_answer != correct_answer:
                    button.background_color = (0.7, 0.1, 0.1, 1)
                    button.background_disabled_normal = ''
                    button.disabled_color = (1, 1, 1, 1)
                else:
                    button.background_color = (0.2, 0.6, 1, 1)
                    button.background_disabled_normal = ''
                    button.disabled_color = (1, 1, 1, 1)

                #отключаем все кнопки
                button.disabled = True

            #обновляем счет
            if selected_answer == correct_answer:
                self.score += 1
                timer_duration = 1
            else:
                timer_duration = 3

            self.score_label.text = f'Счет: {self.score}/{len(self.questions)}'

            #таймер для автоматического перехода
            from kivy.clock import Clock
            Clock.schedule_once(lambda dt: self.next_question(), timer_duration)
        def next_question(self):
            # если осталось время - след вопрос
            if hasattr(self, 'timer_active') and self.timer_active and self.time_left <= 0:
                print("⏰ Время вышло! Завершаем квиз")
                self.show_final_results()
                return

            self.current_question += 1
            self.load_question()

        def show_final_results(self):
            if hasattr(self, 'timer_event') and self.timer_active:
                self.timer_event.cancel()
                self.timer_active = False

            self.layout.clear_widgets()

            total_questions = len(self.questions)
            percentage = (self.score / total_questions) * 100 if total_questions > 0 else 0

            # сохранение только для вопросов по темам
            if "20 случайных вопросов" not in self.current_theme_name:
                app = App.get_running_app()
                app.save_theme_progress(self.current_theme_name, self.score, total_questions)

            from kivy.uix.floatlayout import FloatLayout

            main_layout = FloatLayout()

            result_container = BoxLayout(
                orientation='vertical',
                padding=15,
                spacing=8,
                size_hint=(0.7, 0.35),
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )

            with result_container.canvas.before:
                Color(0.95, 0.95, 0.95, 1)
                self.bg_rect = RoundedRectangle(
                    pos=result_container.pos,
                    size=result_container.size,
                    radius=[15, 15, 15, 15]
                )

            def update_bg(instance, value):
                instance.canvas.before.clear()
                with instance.canvas.before:
                    Color(0.95, 0.95, 0.95, 1)
                    RoundedRectangle(
                        pos=instance.pos,
                        size=instance.size,
                        radius=[15, 15, 15, 15]
                    )

            result_container.bind(pos=update_bg, size=update_bg)

            title_label = Label(
                text='Результат',
                font_size='24sp',
                size_hint=(1, 0.35),
                color=(0.1, 0.4, 0.8, 1)
            )
            result_container.add_widget(title_label)

            if percentage == 100:
                message = f'Идеально! {self.score}/{total_questions}'
            elif percentage >= 75:
                message = f'Отлично {self.score}/{total_questions}'
            elif percentage >= 50:
                message = f'Хорошо {self.score}/{total_questions}'
            else:
                message = f'Следует повторить {self.score}/{total_questions}'

            result_label = Label(
                text=message,
                font_size='18sp',
                size_hint=(1, 0.4),
                halign='center',
                valign='middle',
                color=(0.2, 0.2, 0.2, 1)
            )
            result_container.add_widget(result_label)

            buttons_layout = BoxLayout(
                orientation='horizontal',
                spacing=6,
                size_hint=(1, 0.2)
            )

            blue_color = (0.2, 0.6, 1, 1)

            if self.current_theme_name != "20 случайных вопросов":
                retry_btn = Button(
                    text='Ещё раз',
                    background_color=blue_color,
                    color=(1, 1, 1, 1),
                    font_size='18sp'
                )
                retry_btn.bind(on_press=self.retry_theme_direct)
                buttons_layout.add_widget(retry_btn)

            menu_btn = Button(
                text='Меню',
                background_color=blue_color,
                color=(1, 1, 1, 1),
                font_size='18sp'
            )
            menu_btn.bind(on_press=self.return_to_menu_direct)
            buttons_layout.add_widget(menu_btn)

            result_container.add_widget(buttons_layout)
            main_layout.add_widget(result_container)
            self.layout.add_widget(main_layout)

        def return_to_menu_direct(self, instance):
            app = App.get_running_app()
            app.screen_manager.current = 'menu'

        def retry_theme_direct(self, instance):
            app = App.get_running_app()
            theme_questions = app.themes[self.current_theme_name]['questions']
            app.start_quiz(theme_questions, self.current_theme_name)

        def return_to_menu(self, instance):
            app = App.get_running_app()
            app.screen_manager.current = 'menu'

        def retry_theme(self, instance):
            app = App.get_running_app()
            theme_questions = app.themes[self.current_theme_name]
            app.start_quiz(theme_questions, self.current_theme_name)


    class QuestionManager:
        def __init__(self):
            self.themes = {}
            self.all_questions = []

        def load_questions(self):
            #загрузка вопросов из файлов
            try:
                #Загрузка тем
                manifest_path = self.get_data_path('themes_manifest.json')
                print(f"DEBUG: Manifest path: {manifest_path}")
                print(f"DEBUG: Manifest exists: {os.path.exists(manifest_path)}")
                if not os.path.exists(manifest_path):
                    Logger.error(f"QuestionManager: Manifest not found at {manifest_path}")
                    return False

                with open(manifest_path, 'r', encoding='utf-8') as f:
                    themes_manifest = json.load(f)

                print(f"DEBUG: Manifest loaded, {len(themes_manifest)} themes found")

                #Загрузка вопросов для каждой темы
                for theme_info in themes_manifest:
                    theme_name = theme_info['name']

                    # аходим номер темы из манифеста
                    theme_index = themes_manifest.index(theme_info) + 1
                    theme_file = f"theme{theme_index}.json"
                    theme_path = self.get_data_path(theme_file)

                    print(f"DEBUG: Loading theme {theme_index}: {theme_name}")
                    print(f"DEBUG: Theme path: {theme_path}")
                    print(f"DEBUG: Theme exists: {os.path.exists(theme_path)}")

                    if os.path.exists(theme_path):
                        with open(theme_path, 'r', encoding='utf-8') as f:
                            questions = json.load(f)

                        print(f"DEBUG: Loaded {len(questions)} questions for {theme_name}")

                        self.themes[theme_name] = {
                            'folder': theme_info['folder'],
                            'questions': questions
                        }

                        self.all_questions.extend(questions)
                        Logger.info(f"QuestionManager: Loaded {len(questions)} questions for {theme_name}")
                    else:
                        Logger.error(f"QuestionManager: Questions file not found: {theme_path}")

                Logger.info(f"QuestionManager: Total themes loaded: {len(self.themes)}")
                Logger.info(f"QuestionManager: Total questions: {len(self.all_questions)}")
                return True

            except Exception as e:
                Logger.error(f"QuestionManager: Error loading questions: {e}")
                return False

        def get_data_path(self, filename):
            #найти путь к файлам
            from kivy.utils import platform
            if platform == 'android':
                return filename
            else:
                return os.path.join('data', filename)

        def get_theme_questions(self, theme_name):
            #найти вопросы по названию
            return self.themes.get(theme_name, {}).get('questions', [])

        def get_theme_folder(self, theme_name):
            #найти папку с картинками от вопросов
            return self.themes.get(theme_name, {}).get('folder', '')

        def get_all_questions(self):
            #сами вопросы
            return self.all_questions

        def get_available_themes(self):
            return list(self.themes.keys())
    class QuizApp(App):
        def __init__(self):
            super().__init__()

            super().__init__()

            self.question_manager = QuestionManager()
            self.themes = {}
            self.all_questions = []

            print("DEBUG: Starting QuizApp initialization...")

            if not self.question_manager.load_questions():
                print("DEBUG: Question loading FAILED")
                # Просто создаем пустые данные если не загрузилось
                self.themes = {}
                self.all_questions = []
            else:
                print("DEBUG: Question loading SUCCESS")
                self.themes = self.question_manager.themes
                self.all_questions = self.question_manager.all_questions
                print(f"DEBUG: Loaded {len(self.themes)} themes")
                print(f"DEBUG: Loaded {len(self.all_questions)} total questions")
            self.progress_data = {}
            self.load_progress()

        print("DEBUG: QuizApp initialization completed")

        def get_app_storage_path(self):
            from kivy.utils import platform
            #нахождение файлов на андроид
            if platform == 'android':
                try:
                    from android.storage import app_storage_path
                    return app_storage_path()
                except ImportError:
                    return os.getcwd()
            else:
                return os.getcwd()

        def get_image_path(self, filename, theme_folder=''):
            from kivy.utils import platform

            if platform == 'android':
                #На Android используем относительные пути
                if theme_folder and filename:
                    return os.path.join(theme_folder, filename)
                elif filename:
                    return filename
                else:
                    return 'No_image.jpg'
            else:
                #На ПК используем обычные пути
                if theme_folder and filename:
                    possible_paths = [
                        os.path.join(theme_folder, filename),
                        os.path.join('images', theme_folder, filename),
                        os.path.join('Images', theme_folder, filename),
                        os.path.join('images', filename),
                        os.path.join('Images', filename),
                        filename,
                    ]

                    for image_path in possible_paths:
                        if os.path.exists(image_path):
                            return image_path

                    #нету файла - используем заглушку
                    return self.get_no_image_path()
                elif filename:
                    return filename
                else:
                    return self.get_no_image_path()

        def get_no_image_path(self):
            #найти заглушку
            from kivy.utils import platform

            if platform == 'android':
                return 'No_image.jpg'
            else:
                possible_paths = [
                    'No_image.jpg',
                    'Images/No_image.jpg',
                    'images/No_image.jpg',
                    os.path.join(os.path.dirname(__file__), 'No_image.jpg')
                ]

                for image_path in possible_paths:
                    if os.path.exists(image_path):
                        return image_path

                return ''

        def get_progress_file_path(self):
            #сохранение прогресса для андроид/пк (пк для теста, мне лень убирать)
            from kivy.utils import platform

            if platform == 'android':
                try:
                    from android.storage import app_storage_path
                    storage_path = app_storage_path()
                    progress_path = os.path.join(storage_path, 'quiz_progress.json')
                    print(f"📁 Путь к прогрессу на Android: {progress_path}")
                    return progress_path
                except ImportError:
                    print("⚠️ Не удалось получить android storage, используем текущую директорию")
                    return 'quiz_progress.json'
            else:
                return 'quiz_progress.json'

        def build(self):
            #менеджер экранов
            self.screen_manager = ScreenManager()

            self.menu_screen = MenuScreen(name='menu')
            self.themes_screen = ThemesScreen(name='themes')
            self.quiz_screen = QuizScreen(name='quiz')

            self.screen_manager.add_widget(self.menu_screen)
            self.screen_manager.add_widget(self.themes_screen)
            self.screen_manager.add_widget(self.quiz_screen)

            #Показываем меню при запуске
            return self.screen_manager

        def start_quiz(self, questions, title):
            shuffled_questions = questions.copy()
            random.shuffle(shuffled_questions)
            self.quiz_screen.setup_quiz(shuffled_questions, title)
            self.screen_manager.current = 'quiz'

        def load_progress(self):
            #загрузка прогресса ищ файла
            file_path = self.get_progress_file_path()

            try:
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        self.progress_data = json.load(f)
                    print("Прогресс загружен")
                else:
                    self.progress_data = {}
                    print(" Файл прогресса не найден, создаем новый")
            except Exception as e:
                print(f"Ошибка загрузки прогресса: {e}")
                self.progress_data = {}

        def save_progress(self):
            #сохранение прогресса
            try:
                file_path = self.get_progress_file_path()
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.progress_data, f, ensure_ascii=False, indent=2)
                print("Прогресс сохранен")
            except Exception as e:
                print(f"Ошибка сохранения прогресса: {e}")

        def save_theme_progress(self, theme_name, score, total_questions):
            #прогресс по определенной теме
            if theme_name not in self.progress_data:
                self.progress_data[theme_name] = {
                    'best_score': score,
                    'total_questions': total_questions,
                    'attempts': 1
                }
            else:
                current_best = self.progress_data[theme_name]['best_score']
                if score > current_best:
                    self.progress_data[theme_name]['best_score'] = score
                self.progress_data[theme_name]['attempts'] += 1

            self.save_progress()
            print(f"Сохранен прогресс по теме '{theme_name}': {score}/{total_questions}")

        def get_theme_progress(self, theme_name):
            if theme_name in self.progress_data:
                return self.progress_data[theme_name]
            else:
                return {
                    'best_score': 0,
                    'total_questions': len(self.themes[theme_name]['questions']),
                    'attempts': 0
                }

        def create_styled_button(self, text, color, height=60, font_size='16sp'):
            from kivy.graphics import Color, RoundedRectangle
            btn = Button(
                text=text,
                font_size=font_size,
                size_hint_y=None,
                height=height,
                background_color=color,
                background_normal='',
                background_down='',
                color=(1, 1, 1, 1)
            )

            btn.original_color = color

            #Добавляем скругленные углы
            with btn.canvas.before:
                Color(color[0], color[1], color[2], color[3])
                btn.rect = RoundedRectangle(
                    size=btn.size,
                    pos=btn.pos,
                    radius=[15,15,15,15]  #Скругление углов
                )

            def update_rect(instance, value):
                instance.rect.pos = instance.pos
                instance.rect.size = instance.size

            btn.bind(pos=update_rect, size=update_rect)
            return btn

    if __name__ == '__main__':
        QuizApp().run()

except Exception as e:
    # Умная запись ошибки
    debug_dir = '/storage/emulated/0/Download' if os.path.exists('/storage/emulated/0/Download') else '.'
    error_file = os.path.join(debug_dir, 'debug_error.txt')

    with open(error_file, 'w') as f:
        f.write(f"ОШИБКА: {str(e)}\n")
        f.write(traceback.format_exc())