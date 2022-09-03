# new imports!
import googleapiclient.discovery
import google_auth_oauthlib.flow
import sys
import pandas as pd

current_credential = 0


def get_authenticated_service(credential_path):
    '''
    Takes in a path to a json-file holding oauth credentials for YouTubes v3 API
    After authentication in the browser, it returns an authenticated service 
    '''
    api_service_name = "youtube"
    api_version = "v3"

    client_secrets_file = credential_path
    scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

    # API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)

    credentials = flow.run_local_server(host='localhost',
                                        port=8080,
                                        authorization_prompt_message='Please visit this URL: {url}',
                                        success_message='The auth flow is complete; you may close this window.',
                                        open_browser=True)

    return (googleapiclient.discovery.build(api_service_name,
                                            api_version,
                                            credentials=credentials))


def get_video_info(authenticated_service, id, credential_paths):
    '''
    Function to retrieve the information we need from the API 
    Takes an authenticated service and a video id
    '''
    request = authenticated_service.videos().list(
        part='snippet',
        id=id,
        fields='items(snippet(description)),items(snippet(thumbnails(high(url)))),\
        items(snippet(publishedAt)),items(snippet(tags))items(snippet(channelId))'
    )

    try:
        return request.execute(), credential_paths

    except googleapiclient.errors.HttpError as e:
        print(e)
        if e.error_details[0]['reason'] == 'quotaExceeded':
            try:
                # close the current connection
                youtube.close()

                # get a new set of credentials and try to activate it! 
                creds = credential_paths.pop()
                youtube = get_authenticated_service(creds)

                print(f'Having trouble with {id=}, trying credential {current_credential}')
                get_video_info(youtube, id, credential_paths)

            except IndexError:
                print('Ran out of credentials! Trying again from the beginning')
                get_video_info(youtube, id, ['credentials/credentials1.json',
                                             'credentials/credentials2.json',
                                             'credentials/credentials3.json'])


def parse_video_response(response):
    '''
    retrieves video info from a response object
    returns them individually. 
    '''
    response = response['items'][0]['snippet']  # gets only the snippet dict!
    description = response.get('description', pd.NA)
    channel_id = response.get('channelId', pd.NA)
    published_at = response.get('publishedAt', pd.NA)
    thumbnail = response.get(
        'thumbnails', pd.NA
    ).get(
        'high', pd.NA
    ).get(
        'url', pd.NA
    )
    tag = response.get('tags', pd.NA)

    return description, channel_id, published_at, thumbnail, tag


def main():
    channel_ids = []
    published_at = []
    descriptions = []
    thumbnails = []
    tags = []
    removed_videos_ids = []

    credentials = [
        'credentials/credentials1.json',
        'credentials/credentials2.json',
        'credentials/credentials3.json'
    ]

    if len(sys.argv) < 1:
        raise SystemExit(f"Usage: {sys.argv[0]} <path_to_df>")

    path_to_df = sys.argv[1]

    df = pd.read_csv(path_to_df, index_col=0)

    youtube = get_authenticated_service('credentials/credentials1.json')

    for i, id in enumerate(df.video_id):
        response, credentials = get_video_info(youtube, id, credentials)
        
        if response['items']:
            description, channel_id, published, thumbnail, tag = parse_video_response(
                response)
            channel_ids.append(channel_id)
            published_at.append(published)
            descriptions.append(description)
            thumbnails.append(thumbnail)
            tags.append(tag)
        else:
            removed_videos_ids.append(id)
            print(
                f'Video number {i=} with {id=} did not have any information!j')

    # fjern de id'er der ikke kan fås information på
    full_df = df[~df['video_id'].isin(removed_videos_ids)]
    # tilføj de nye lister som kolonner i en samlet df
    full_df = full_df.assign(
        channel_id=channel_ids,
        published_date=published_at,
        description=descriptions,
        thumbnail=thumbnails,
        tag=tags
    )

    full_df.to_csv('Renset data/history_w_videoinfo_test.csv')


if __name__ == "__main__":
    main()
