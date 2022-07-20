import scrapetube
from youtube_transcript_api import YouTubeTranscriptApi

numberOfVideosToSearch = 2


def main():
    allVideos = scrapetube.get_channel("UC4JX40jDee_tINbkjycV4Sg")
    videoIds = []

    for videoIndex, video in enumerate(allVideos):
        if videoIndex >= numberOfVideosToSearch:
            break

        videoIds.append(video["videoId"])

    transcripts = YouTubeTranscriptApi.get_transcripts(videoIds)


main()
