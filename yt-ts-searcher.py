import scrapetube
from youtube_transcript_api import YouTubeTranscriptApi
import re

searchTerm = "anyways"
numberOfVideosToSearch = 3
channelToSearch = "UC4JX40jDee_tINbkjycV4Sg"


def main():
    allVideos = scrapetube.get_channel(channelToSearch)
    videoIds = []

    for videoIndex, video in enumerate(allVideos):
        if videoIndex >= numberOfVideosToSearch:
            break

        videoIds.append(video["videoId"])

    transcripts = YouTubeTranscriptApi.get_transcripts(videoIds)
    # todo use numpy
    transcripts = transcripts[0]

    searchTermOccurrences = {}

    for videoId in videoIds:
        videoTranscript = transcripts[videoId]
        searchTermVideoOccurrences = searchVideoTranscript(searchTerm, videoTranscript)
        if searchTermVideoOccurrences:
            searchTermOccurrences[videoId] = searchTermVideoOccurrences

    for videoId in videoIds:
        if videoId in searchTermOccurrences:
            video = searchTermOccurrences[videoId]
            print()
            print(videoId)
            for occurrence in video:
                print(f'Start: {occurrence["start"]}')
                print(f'Text: {occurrence["text"]}')
            print()


def searchVideoTranscript(searchTerm, videoTranscript):
    # todo use numpy
    searchTermVideoOccurrences = []

    # todo use numpy
    for transcriptSection in videoTranscript:
        transcriptSectionText = transcriptSection["text"]

        if transcriptSectionText == "[Music]":
            continue

        searchTermResult = re.search(searchTerm, transcriptSectionText)
        if searchTermResult:
            searchTermVideoOccurrences.append(transcriptSection)

    return searchTermVideoOccurrences


main()
