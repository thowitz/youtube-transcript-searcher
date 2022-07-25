import scrapetube
from youtube_transcript_api import YouTubeTranscriptApi
import typer
import re
import numpy as np
import requests
import time

languages = ["en", "en-UK", "en-US", "en-CA"]


def main(searchTerm, channelUsername, numberOfVideos):
    startTime = time.time()

    videoIds = getVideoIds(channelUsername, numberOfVideos)

    transcripts = YouTubeTranscriptApi.get_transcripts(
        videoIds, languages=languages, continue_after_error=True
    )
    failedTranscripts = transcripts[1]
    transcripts = transcripts[0]

    searchTermOccurrences = {}
    numberOfOccurrences = 0

    for videoId in videoIds:
        if videoId in transcripts:
            videoTranscript: list = transcripts[videoId]
            searchTermVideoOccurrences = searchVideoTranscript(
                searchTerm, videoTranscript
            )
            if searchTermVideoOccurrences:
                searchTermOccurrences[videoId] = searchTermVideoOccurrences
                numberOfOccurrences += len(searchTermVideoOccurrences)

    finishTime = time.time()

    printOccurrences(
        videoIds,
        searchTermOccurrences,
    )

    printMetadata(
        numberOfOccurrences,
        failedTranscripts,
        searchTerm,
        channelUsername,
        numberOfVideos,
        startTime,
        finishTime,
    )


def typerHelper(
    searchterm: str = typer.Option(
        ...,
        "--search-term",
        "-t",
        help="Term to search for",
        rich_help_panel="Search Options",
        prompt="Please enter the search term",
    ),
    channelusername: str = typer.Option(
        ...,
        "--channel-username",
        "-u",
        help="The username of the channel to search, found in the address bar of the channel page",
        rich_help_panel="Search Options",
        prompt="Please enter the channel username",
    ),
    numberofvideos: int = typer.Option(
        10,
        "--number-of-videos",
        "-n",
        help="The number of videos to search through, from latest to oldest",
        rich_help_panel="Search Options",
        prompt="Please enter the number of videos to search through",
    ),
):
    main(
        searchTerm=searchterm,
        channelUsername=channelusername,
        numberOfVideos=numberofvideos,
    )


def getVideoIds(channelUsername, numberOfVideos):
    channelId = getChannelIdFromUsername(channelUsername)

    allVideos = scrapetube.get_channel(channelId)
    videoIds = []

    for videoIndex, video in enumerate(allVideos):
        if videoIndex >= numberOfVideos:
            break

        videoIds.append(video["videoId"])

    return videoIds


def getChannelIdFromUsername(channelUsername):
    channelResponse = requests.get(
        f"https://youtube.com/c/{channelUsername}?cbrd=1&ucbcb=1"
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


def printOccurrences(
    videoIds,
    searchTermOccurrences,
):

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


def printMetadata(
    numberOfOccurrences,
    failedTranscripts,
    searchTerm,
    channelUsername,
    numberOfVideos,
    startTime,
    finishTime,
):
    if failedTranscripts:
        print("Failed to retrieve transcripts for:")
        for failedTranscript in failedTranscripts:
            print(failedTranscript)

    print()
    print(f"[+] Finished searching channel {channelUsername}")
    print(
        f"[+] Searched the latest {numberOfVideos} video(s) for the term {searchTerm}"
    )
    print(
        f"[+] Found {numberOfOccurrences} occurrence(s) in {round(finishTime-startTime)}s"
    )
    print(f"[+] Failed to check {len(failedTranscripts)} transcript(s)")


if __name__ == "__main__":
    typer.run(typerHelper)
