import scrapetube
from youtube_transcript_api import YouTubeTranscriptApi
import re
import numpy as np
import requests
import time

searchTerm = "anyways"
numberOfVideosToSearch = 10
channelUsernameToSearch = "techwithtim"
languages = ["en", "en-UK", "en-CA"]


def main():
    startTime = time.time()

    channelIdToSearch = getChannelIdFromUsername(channelUsernameToSearch)

    allVideos = scrapetube.get_channel(channelIdToSearch)
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

    finishTime = time.time()

    occurrenceNumber = 1
    for videoId in videoIds:
        if videoId in searchTermOccurrences:
            video = searchTermOccurrences[videoId]
            print()
            print(f"#{occurrenceNumber}")
            print(videoId)
            print(f"https://youtube.com/watch?v={videoId}")
            for occurrence in video:
                startTimeTotalSeconds = round(occurrence["start"] - 1)
                startTimeMinutes = int(startTimeTotalSeconds / 60)
                startTimeSeconds = startTimeTotalSeconds % 60

                print(f"Start: {startTimeMinutes}:{startTimeSeconds}")
                print(f'Text: {occurrence["text"]}')
            print()
            occurrenceNumber += 1

    if failedTranscripts:
        print("Failed to retrieve transcripts for:")
        for failedTranscript in failedTranscripts:
            print(failedTranscript)

    print()
    print(f"[+] Finished searching channel {channelUsernameToSearch}")
    print(
        f"[+] Searched the latest {numberOfVideosToSearch} videos for the term {searchTerm}"
    )
    print(
        f"[+] Found {len(searchTermOccurrences)} occurrences in {round(finishTime-startTime)}s"
    )
    print(f"[+] Failed to check {len(failedTranscripts)} transcripts")


def getChannelIdFromUsername(channelNameToSearch):
    channelResponse = requests.get(
        f"https://youtube.com/c/{channelNameToSearch}?cbrd=1&ucbcb=1"
    )
    channelSource = str(channelResponse.content)
    channelIdSearchResult = re.search("externalId", channelSource)
    if channelIdSearchResult:
        startOfChannelId = channelIdSearchResult.span()[1] + 3
        channelId = channelSource[startOfChannelId : startOfChannelId + 24]
        return channelId
    else:
        raise Exception("Channel id not found from source code")


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
