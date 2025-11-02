[app]
title = ПДД практика
package.name = smartquizpdd
package.domain = ru.andf.smartquiz

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json

# Включите папки с данными
source.include_dirs = data, images

version = 1.0
requirements = python3,kivy,requests,pillow,android

# Разрешения Android
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Версии Android
android.api = 33
android.minapi = 21
android.ndk = 25b

# Архитектура
android.arch = arm64-v8a,armeabi-v7a

orientation = portrait
fullscreen = 0

# Иконка и заставка
icon.filename = icon.png
presplash.filename = presplash.png

# Оптимизация для GitHub Actions
android.accept_sdk_license = True

[buildozer]
log_level = 2