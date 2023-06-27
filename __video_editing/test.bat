echo off
set arg1=%1
shift
for /f %%i in ('yt-dlp -f b -g 'https://www.youtube.com/watch?v=%arg1% ' --extractor-args youtube:player-skip=js') do set result=%%i
echo %result%
