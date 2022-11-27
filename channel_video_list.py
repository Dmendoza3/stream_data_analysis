import requests

API_KEY = "AIzaSyBEWI-LTE_xOqSS9oGm8i9YUFKM_voSB8E" #tester_api_key_1
#API_KEY = "AIzaSyDxT3U4v6ScAGQdhT9BS3l2BmJUKSmOPB8" #tester_api_key_2
#API_KEY = "AIzaSyBj06Z7lWI842PIC56xrL5e9pQ0XL7cdwk" #tester_api_key_3
#API_KEY = "AIzaSyARDn0KG6PCwOl9QvfWlC4HenC9gtqp7Dk" #tester_api_key_4


def get_channel_video_info_id(channel_id):
    url = "https://www.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails&id=" + channel_id + "&key=" + API_KEY
    response = requests.get(url)

    video_playlist_id = response.json()
    channel_name = video_playlist_id["items"][0]["snippet"]["title"]
    uploads = video_playlist_id["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    video_list = get_all_videos_id(uploads)

    return (channel_name, video_list)


def get_all_videos_id(playlist_id):
    next_token = "start"
    video_list = []

    while next_token:
        next_token = "" if next_token == "start" else next_token

        url = "https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults=50&playlistId=" + playlist_id + "&key=" + API_KEY + ("&pageToken=" + next_token if next_token != "" else "")
        response = requests.get(url)
        response_json = response.json()

        next_token = response_json.get("nextPageToken", "")

        for item in response_json["items"]:
            video_list.append(item["contentDetails"]["videoId"])

    return video_list

def get_video_info(video_id, full_json = False):
    url = "https://youtube.googleapis.com/youtube/v3/videos?part=snippet%2CliveStreamingDetails%2CcontentDetails&id=" + video_id + "&key=" + API_KEY
    #%2Cstatistics
    response = requests.get(url)
    response_json = response.json()

    if full_json:
        return response_json
    else:
        video_name = response_json["items"][0]["snippet"]["title"]
        clean_name = ("".join(list(filter(lambda ch: ord(ch) in range(1, 128) and (ch not in ".<>:\"/\\|?*"), video_name)))).replace(" ", "_")

        start_time = response_json["items"][0].get("liveStreamingDetails", {"actualStartTime":""})["actualStartTime"]
        end_time = response_json["items"][0].get("liveStreamingDetails", {"actualEndTime":""})["actualEndTime"]

        return {"video_name":video_name, "clean_name": clean_name, "start_time": start_time, "end_time":end_time, "video_id": video_id}


if __name__ == "__main__":
    video_id_list = ["pXH5BZViSOM"]
    for video_id in video_id_list:
        print(str(get_video_info(video_id, full_json=True)).replace("'",'"').replace('"nis', "'nis"), file=open("clip_example_" + video_id + ".json", "w", encoding="utf-8"))