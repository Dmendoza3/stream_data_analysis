import csv

from youtube_transcript_api import YouTubeTranscriptApi

video_id = "qKjKUSZHrcA"

transcript = YouTubeTranscriptApi.get_transcript(video_id)
#transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

o_file= open("transcript_" + video_id + ".csv", "w", encoding="utf-8")

headers = ['text','start','duration']

csv_o_file = csv.DictWriter(o_file, fieldnames=headers, lineterminator="\n")

csv_o_file.writeheader()
csv_o_file.writerows(transcript)