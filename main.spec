# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['/Users/patrick/dev/pktrader'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='PKTrader',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
app = BUNDLE(exe,
             name='PKTrader.app',
             icon=None,
             bundle_identifier=None,
             info_plist={
                'NSHighResolutionCapable': True,
                'CFBundleIdentifier': 'com.vedanamedia.pktrader',
                'CFBundleName': 'PKTrader'
             })
