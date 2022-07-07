import scrapetube
from youtube_transcript_api import YouTubeTranscriptApi

numberOfVideosToSearch = 2


def main():
    allVideos = scrapetube.get_channel("UC4JX40jDee_tINbkjycV4Sg")
    videoIds = []

    counter = 0
    for video in allVideos:
        if counter > numberOfVideosToSearch:
            break

        videoIds.append(video["videoId"])
        counter += 1

    transcripts = YouTubeTranscriptApi.get_transcripts(videoIds)


main()
