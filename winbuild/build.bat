del /F /S /Q build
swig -DWIN32 -DWin64 -I%LSF_INCLUDE% -I%LSF_INCLUDE%\lsf -python ..\pythonlsf\lsf.i
msbuild lsf.sln -property:Configuration=Release
mkdir build
cp X64\Release\_lsf.pyd build\
cp X64\Release\_lsf.lib build\
cp X64\Release\_lsf.exp build\
cp ..\pythonlsf\lsf.py build\
del /F /S /Q x64

