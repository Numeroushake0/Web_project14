@ECHO OFF

REM Windows batch file for Sphinx documentation

set SPHINXBUILD=sphinx-build
set SOURCEDIR=source
set BUILDDIR=build
set SPHINXOPTS=

if "%SPHINXBUILD%" == "" (
    set SPHINXBUILD=sphinx-build
)

echo.
echo Building HTML documentation...
%SPHINXBUILD% -b html %SPHINXOPTS% %SOURCEDIR% %BUILDDIR%
echo.
echo Build finished. The HTML pages are in %BUILDDIR%.
