# -*- mode: python -*-

block_cipher = None


a = Analysis(['/Users/cruor/code/sadpandareader/app/main.py'],
             pathex=['/Users/cruor/code/sadpandareader/app'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['_tkinter', 'Tkinter', 'enchant', 'twister'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='sadpanda',
          debug=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe, Tree('/Users/cruor/code/sadpandareader/app/'),
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='sadpanda')
app = BUNDLE(coll,
             name='sadpanda.app',
             icon=None,
             bundle_identifier=None)
