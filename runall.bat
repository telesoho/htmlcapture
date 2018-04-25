@echo off

rem set _BASE_DIR
FOR /F "usebackq delims==" %%i IN (`cd`) DO set _BASE_DIR=%%i

rem set _JAVAPATH
set _JAVAPATH=%_BASE_DIR%\jre1.8.0_102\bin\java.exe


rem call screenshot.bat
set _SCREENSHOT_INPUT_DIR=%_BASE_DIR%\data\html
set _SCREENSHOT_OUTPUT_DIR=%_BASE_DIR%\data\screenshot

cd screenshot\bat
 call htmlcap %_SCREENSHOT_INPUT_DIR% %_SCREENSHOT_OUTPUT_DIR%
cd ../..

 for /f "usebackq tokens=1 delims=." %%a in (`dir %_SCREENSHOT_OUTPUT_DIR%\*.png /b`)  do  md %_SCREENSHOT_OUTPUT_DIR%\%%a\Material & move %_SCREENSHOT_OUTPUT_DIR%\%%a.png  %_SCREENSHOT_OUTPUT_DIR%\%%a\Material

rem ++++++++++++++++++++++++++++++++++++++++
rem + 第1引数：ソースフォルダ(必須)
rem ++++++++++++++++++++++++++++++++++++++++
set _resize_source_dir=%_SCREENSHOT_OUTPUT_DIR%

rem ++++++++++++++++++++++++++++++++++++++++
rem + 第2引数：出力フォルダ(必須)
rem +++++++++++++++++++++++++++++++++++++++
set _resize_output_dir=%_BASE_DIR%\data\resize

rem ++++++++++++++++++++++++++++++++++++++++
rem + 第3引数：リサイズフラグ(必須) ※幅790にリサイズする
rem ++++++++++++++++++++++++++++++++++++++++
set _resize_flag=false

rem ++++++++++++++++++++++++++++++++++++++++
rem + 第4引数：トリミングフラグ(必須) ※縦1540超える場合、1540毎にトリミングする。横が790までトリミングする
rem ++++++++++++++++++++++++++++++++++++++++
set _resize_trim_flag=true

rem ****** 以降は実行コマンドです。必要のない限り修正しないでください。******
set _JARPATH=.\resize_tool\libs\resize.jar
 %_JAVAPATH% -jar %_JARPATH% %_resize_source_dir% %_resize_output_dir% %_resize_flag% %_resize_trim_flag%

set _RESULT_DIR=%_BASE_DIR%\data\result

rem copy image to result folder
for /f "usebackq tokens=1 delims=." %%a in (`dir %_resize_output_dir% /ad /b`)  do xcopy /s /e %_SCREENSHOT_INPUT_DIR%\src\images\%%a %_RESULT_DIR%\%%a\ & rd /s /q %_RESULT_DIR%\%%a\Material & xcopy /s /e %_resize_output_dir%\%%a %_RESULT_DIR%\%%a\

pause