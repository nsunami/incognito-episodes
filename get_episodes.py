import json
import requests


def get_episodes(page_number=1):
    """
    Fetches episodes from the iWantTFC API.

    :param page_number: The page number to fetch. Default is 1.
    :return: A list of episodes.
    """
    # Define the URL
    url = "https://api.iwanttfc.com/consumer/graphql"

    # Define headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:141.0) Gecko/20100101 Firefox/141.0",
        "Accept": "application/graphql-response+json",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Referer": "https://web.iwanttfc.com/",
        "Content-Type": "application/json",
        "x-country-code": "NL",
        "x-device-platform": "web",
        "x-device-subplatform": "firefox",
        "x-iw-useragent": "Name=iwant; Version=1.0.0; \
                           Platform=Web; OSVersion=14.0.0 Model=Chrome; BuildType=debug Environment=development",
        "Origin": "https://web.iwanttfc.com",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "DNT": "1",
        "Sec-GPC": "1",
        "Priority": "u=0",
        "TE": "trailers",
    }

    # Define the data (query and variables)
    data = {
        "query": "query TvShowEpisodes($tvShowEpisodesId: ID, $filters: TvShowEpisodesFilterInput, $skus: [String!]) {\n  tvShowEpisodes(id: $tvShowEpisodesId, filters: $filters, skus: $skus) {\n    items {\n      id\n      assetType\n      title\n      shortDescription\n      images {\n        landscape\n        landscapeHero\n        portrait\n        portraitHero\n        title\n        square\n      }\n      isPlayable\n      duration\n      durationInSeconds\n      labels {\n        id\n        position\n        url\n      }\n      trailerUrls {\n        dash {\n          url\n        }\n      }\n      genres\n      releaseDate\n      earlyAccessDate\n      cast\n      contentDescriptors\n      contentOwner\n      durationInMs\n      directors\n      languages\n      originalLanguage\n      rating\n      videoQuality {\n        id\n        label\n      }\n      audioQuality {\n        id\n        label\n      }\n      subtitleLanguages\n      subHeader\n      subHeaders\n      showInfo {\n        id\n        title\n        tvShowType\n        images {\n          landscape\n          landscapeHero\n          portrait\n          portraitHero\n          title\n          square\n        }\n      }\n      tvShowDetails {\n        totalSeasons\n        tvShowType\n        defaultEpisode {\n          id\n          title\n          subHeader\n          onAirDate\n        }\n      }\n      monetization {\n        type\n        logoUrl\n        hasSkuAccess\n      }\n      seasons {\n        id\n        title\n        count\n        filter {\n          year\n          month\n          seasonId\n        }\n      }\n      promotionalTag {\n        iconUrl\n        text\n      }\n      continueWatching {\n        playbackPosition\n        audioLang\n        subtitleLang\n        resolution\n        bitrate\n      }\n    }\n    totalItems\n    pageSize\n    currentPage\n    totalPages\n    hasNextPage\n    hasPreviousPage\n  }\n}\n    ",
        "variables": {
            "tvShowEpisodesId": "3e4aa6e3-9b31-4308-ae62-15a4e02dd7f8",
            "filters": {
                "year": None,
                "month": None,
                "seasonId": "1",
                "pageNumber": page_number,
                "pageSize": 100,
            },
            "skus": [],
        },
    }

    # Make the POST request
    response = requests.post(url, headers=headers, json=data)

    items = response.json()["data"]["tvShowEpisodes"]["items"]

    n_episodes = response.json()["data"]["tvShowEpisodes"]["totalItems"]
    total_pages = response.json()["data"]["tvShowEpisodes"]["totalPages"]
    has_next_page = response.json()["data"]["tvShowEpisodes"]["hasNextPage"]
    current_page = response.json()["data"]["tvShowEpisodes"]["currentPage"]

    episodes = []

    for item in items:
        episode = {
            "id": item["id"],
            "item": item["title"],
            "subHeader": item["subHeader"],
            "watch": "https://web.iwanttfc.com/player/" + item["id"],
        }
        episodes.append(episode)

    return {
        "episodes": episodes,
        "n_episodes": n_episodes,
        "current_page": current_page,
        "total_pages": total_pages,
        "has_next_page": has_next_page,
    }


all_episodes = get_episodes(page_number=1)

while all_episodes["has_next_page"]:
    next_page = all_episodes["current_page"] + 1
    next_episodes = get_episodes(page_number=next_page)
    all_episodes["episodes"].extend(next_episodes["episodes"])
    all_episodes["has_next_page"] = next_episodes["has_next_page"]

print(len(all_episodes["episodes"]), " episodes has been fetched.")

# Save file
print("Writing out a JSON file")
with open('episodes.json', 'w', encoding='utf-8') as json_file:
    json.dump(all_episodes["episodes"],
              json_file, indent=4, ensure_ascii=False)
