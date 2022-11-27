import csv

from youtube_transcript_api import YouTubeTranscriptApi

video_ids = ["7z9chAzt_vE"]
label = "gura"

for video_id in video_ids:
    try:
        print("downloading", video_id)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        o_file= open(f"./transcripts/{label}/" + label + "_transcript_" + video_id + ".txt", "w", encoding="utf-8")

        headers = ['text','start','duration']

        csv_o_file = csv.DictWriter(o_file, fieldnames=headers, lineterminator="\n")

        csv_o_file.writeheader()
        get_text = lambda x : [{"text": k["text"]} for k in x]

        csv_o_file.writerows(transcript)
        #csv_o_file.writerows(get_text(transcript))
    except Exception as ex:
        print("error:", ex)
