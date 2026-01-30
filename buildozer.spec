[app]
title = MiPilarcito
package.name = regalo
package.domain = org.amor
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,mp3,wav,json
source.include_patterns = assets/*, user_data/*
version = 0.1
requirements = python3,kivy,pillow
orientation = portrait
fullscreen = 0
android.api = 34
android.minapi = 24
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 0
