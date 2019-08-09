swig -DWIN32 -DWin64 -I%LSF_INCLUDE% -I%LSF_INCLUDE%\lsf -python ..\pythonlsf\lsf.i
msbuild lsf.sln -property:Configuration=Release
cp X64\Release\_lsf.pyd ..\pythonlsf\
cp X64\Release\_lsf.lib ..\pythonlsf\
cp X64\Release\_lsf.exp ..\pythonlsf\


