[app]
title = Cash Flow Minimization
package.name = cashflowminimizer
package.domain = org.lokeshwar
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

requirements = python3,kivy,streamlit,networkx,matplotlib,pywebview,pillow

android.permissions = INTERNET

android.api = 33
android.minapi = 21
android.ndk_api = 21

android.archs = arm64-v8a, armeabi-v7a

fullscreen = 0
orientation = portrait

icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/icon.png