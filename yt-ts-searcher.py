import scrapetube
from youtube_transcript_api import YouTubeTranscriptApi
import re
import numpy as np

searchTerm = "anyways"
numberOfVideosToSearch = 100
channelToSearch = "UC4JX40jDee_tINbkjycV4Sg"
languages = ["en", "en-UK", "en-CA"]


def main():
    allVideos = scrapetube.get_channel(channelToSearch)
    videoIds = []

    for videoIndex, video in enumerate(allVideos):
        if videoIndex >= numberOfVideosToSearch:
            break

        videoIds.append(video["videoId"])

    transcripts = YouTubeTranscriptApi.get_transcripts(
        videoIds, languages=languages, continue_after_error=True
    )
    failedTranscripts = transcripts[1]
    transcripts = transcripts[0]

    searchTermOccurrences = {}

    for videoId in videoIds:
        if videoId in transcripts:
            videoTranscript: list = transcripts[videoId]
            searchTermVideoOccurrences = searchVideoTranscript(
                searchTerm, videoTranscript
            )
            if searchTermVideoOccurrences:
                searchTermOccurrences[videoId] = searchTermVideoOccurrences

    for videoId in videoIds:
        if videoId in searchTermOccurrences:
            video = searchTermOccurrences[videoId]
            print()
            print(videoId)
            print(f"https://youtube.com/watch?v={videoId}")
            for occurrence in video:
                startTimeTotalSeconds = round(occurrence["start"] - 1)
                startTimeMinutes = int(startTimeTotalSeconds / 60)
                startTimeSeconds = startTimeTotalSeconds % 60

                print(f"Start: {startTimeMinutes}:{startTimeSeconds}")
                print(f'Text: {occurrence["text"]}')
            print()

    print("Failed to retrieve transcripts for:")
    for failedTranscript in failedTranscripts:
        print(failedTranscript)


def searchVideoTranscript(searchTerm: str, videoTranscript: list):
    videoTranscriptNumpy = np.array(videoTranscript)
    searchTermVideoOccurrences = []

    for transcriptSection in videoTranscriptNumpy:
        transcriptSectionText = transcriptSection["text"]

        if transcriptSectionText == "[Music]":
            continue

        searchTermResult = re.search(searchTerm, transcriptSectionText)
        if searchTermResult:
            searchTermVideoOccurrences.append(transcriptSection)

    return searchTermVideoOccurrences


main()
