@ECHO OFF

pushd %~dp0

REM Command file for Sphinx documentation.

if "%SPHINXBUILD%" == "" (
    set SPHINXBUILD=sphinx-build
)
set SOURCEDIR=.
set BUILDDIR=_build

%SPHINXBUILD% >NUL 2>NUL
if errorlevel 9009 (
    echo.Sphinx is not installed; run: pip install -r requirements.txt
    exit /b 1
)

if "%1" == "" goto help
if "%1" == "help" goto help
if "%1" == "html" goto html
if "%1" == "clean" goto clean

%SPHINXBUILD% -M %1 "%SOURCEDIR%" "%BUILDDIR%" %SPHINXOPTS% %O%
goto end

:help
%SPHINXBUILD% -M help "%SOURCEDIR%" "%BUILDDIR%" %SPHINXOPTS% %O%
goto end

:html
%SPHINXBUILD% -b html -W --keep-going -n "%SOURCEDIR%" "%BUILDDIR%\html"
goto end

:clean
rmdir /S /Q %BUILDDIR%
goto end

:end
popd
