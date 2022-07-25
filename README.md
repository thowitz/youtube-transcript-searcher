# Youtube transcript searcher

## About

- This is small cli program that searches the transcripts of videos in a youtube channel for a specific term
- I stand on the shoulders of giants, 3 amazing open source projects did most of the work, I just mushed them together. Check out the acknowledgements and give them some love :)

## Usage

**One liner**

- -t {search term}
- -u {channel username}
- -n {number of videos to search}

**Prompt**

- Any options omitted will be prompted for
- So just run the script without any options

## How it works

- The scrapetube library is used to get a list of the video ids, where the length is the number of videos to search for
- The transcripts for the videos in the video ids list are then retrieved using the youtube transcript api library
- Each transcript of each video is checked for the search term and any occurrences are stored
- At the end, the id of each video containing any occurrences is printed along with the text and start position of every occurrence

## Acknowledgements

**Youtube libraries**

These libraries were essential to the project, allowing me to get all the data I needed without having to use selenium or the annoying youtube api

- [Scrapetube](https://github.com/dermasmid/scrapetube)
- [Youtube transcript api](https://github.com/jdepoix/youtube-transcript-api)

**Cli**

- [Typer](https://github.com/tiangolo/typer) is a brilliant library for easily creating clis, I was able to add all the user interaction I wanted in like 5 minutes
