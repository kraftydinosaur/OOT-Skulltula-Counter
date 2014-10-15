# -*- mode: python -*-
a = Analysis(['main.py'],
             pathex=['.'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)

a.datas += [('icon.gif', 'icon.gif',  'DATA')]

pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='OOT Skulltula Counter.exe',
          icon = 'icon.ico',
          debug=False,
          strip=None,
          upx=True,
          console=False )
