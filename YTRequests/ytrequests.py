import requests

class YTRequestsError(Exception):
    pass

class YTArgumentError(Exception):
    pass

class YTRequests:

    base_url = 'https://www.googleapis.com/youtube/v3'
    unofficial_api_key = 'AIzaSyAa8yy0GdcGPHdtD083HiGGx_S0vMPScDM'
    base_headers = {
        "content-type": "application/json"
    }

    def __init__(self, api_key = None, unofficial = False):
        if unofficial:
            self.base_headers["x-origin"] = "https://explorer.apis.google.com"
            self.api_key = self.unofficial_api_key
        elif api_key:
            self.api_key = api_key
        else:
            raise Exception("No API key provided")
    
    # def get_video_info(self, videoId):
    #     params = {

    #     }

    def get_comments(self, videoId):
        params = {
            "part": "id,snippet,replies",
            "maxResults": 50,
            "videoId": videoId,
            "key": self.api_key
        }

        nextToken = None
        items = []

        while True:
            if nextToken:
                params["pageToken"] = nextToken
            r = requests.get(f"{self.base_url}/commentThreads", params=params, headers=self.base_headers)
            if r.status_code != 200:
                if len(items) > 0:
                    return items

                raise YTRequestsError(r.status_code, r.text)

            data = r.json()
            items.extend(data["items"])
            nextToken = data.get("nextPageToken")
            if not nextToken:
                break

        return items

    def search_videos(self, word, max_results=50):
        params = {
            "part": "id,snippet",
            "maxResults": max_results,
            "q": word,
            "key": self.api_key
        }

        nextToken = None
        items = []

        while True:
            if nextToken:
                params["pageToken"] = nextToken
            r = requests.get(f"{self.base_url}/search", params=params, headers=self.base_headers)
            if r.status_code != 200:
                if len(items) > 0:
                    return items

                raise YTRequestsError(r.status_code, r.text)

            data = r.json()
            items.extend(data["items"])
            nextToken = data.get("nextPageToken")
            if not nextToken:
                break

        return items

    def get_video_info(self, _id, parts=None):
        if not parts:
            parts = [
                "id",
                "snippet",
                "contentDetails",
                # "fileDetails",
                "liveStreamingDetails",
                "player",
                # "processingDetails",
                "recordingDetails",
                "statistics",
                "status",
                # "suggestions",
                "topicDetails"
            ]

        if type(parts) == list:
            parts = ",".join(parts)
        elif type(parts) != str:
            raise YTArgumentError("parts must be a list or a string")
        if type(_id) == list:
            _id = ",".join(_id)
        elif type(_id) != str:
            raise YTArgumentError("_id must be a list or a string")
        params = {
            "part": parts,
            "id": _id,
            "key": self.api_key
        }
        r = requests.get(f"{self.base_url}/videos", params=params, headers=self.base_headers)
        if r.status_code != 200:
            raise YTRequestsError(r.status_code, r.text)

        return r.json()["items"]