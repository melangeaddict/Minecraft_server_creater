# Minecraft_server_creater

This script is designed to automate the creation of a Minecraft Server.  Run using:

python3 CreateMCServer.py

It will prompt you for how many servers to create.  It *should* ignore any servers already made using the script.  For example, if this is the first time, you specify how many you want to create.  Say 2.  The script will create a 'minecraft0', and 'minecraft1' folders, then download the latest server release to them.  It will attempt to start them as well.  If you already have servers created, it will skip already-made folders, and create a new one afterwards.  If you already have 2, and want another, specify you want 3 servers created.  It will skip servers 0 and 1, and create 2.  As I write this, I realize that isn't all that helpful, so I will probably change that in the future.

Script is currently untested.