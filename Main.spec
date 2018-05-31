# -*- mode: python -*-

block_cipher = None


a = Analysis(['Main.py'],
             pathex=['D:\\학업관련\\3학년 1학기\\스크립트 언어\\Wetherforecast'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Main',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )
