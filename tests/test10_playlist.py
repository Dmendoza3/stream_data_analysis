import requests

playlistid = "UU8rcEBzJSleTkf_-agPM20g"
next_token = "start"
video_list = []

while next_token:
    next_token = "" if next_token == "start" else next_token

    url = "https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults=50&playlistId=" + playlistid + "&key=AIzaSyBEWI-LTE_xOqSS9oGm8i9YUFKM_voSB8E" + ("&pageToken=" + next_token if next_token != "" else "")
    x = requests.get(url)
    di = x.json()

    next_token = di.get("nextPageToken", "")
    for item in di["items"]:
        video_list.append(item["contentDetails"]["videoId"])

print("video_list", video_list)
print("length", len(video_list))