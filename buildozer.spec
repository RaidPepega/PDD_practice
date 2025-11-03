[app]
title = ПДД практика
package.name = smartquizpdd
package.domain = ru.andf.smartquiz

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,txt
source.include_dirs = data, images

version = 1.0
requirements = python3,kivy,requests,pillow,android

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a,armeabi-v7a

orientation = portrait
fullscreen = 0

icon.filename = icon.png
presplash.filename = presplash.png

android.accept_sdk_license = True