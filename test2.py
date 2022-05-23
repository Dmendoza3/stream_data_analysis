import pytchat

video_id = 'hD6LwW7Zkf8'
chat = pytchat.create(video_id=video_id)

print(chat.is_replay())