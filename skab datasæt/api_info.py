# new imports!
from urllib import response
import googleapiclient.discovery
import google_auth_oauthlib.flow
import sys
import pandas as pd


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

    credentials = flow.run_console()

    return (googleapiclient.discovery.build(api_service_name,
                                            api_version,
                                            credentials=credentials))


def get_video_info(authenticated_service, id, credential_paths):
    '''
    Function to retrieve the information we need from the API
    Takes an authenticated service and a video id
    '''
    request = authenticated_service.videos().list(
        part='snippet,topicDetails',
        id=id,
        fields='items(snippet(description)),items(snippet(thumbnails(high(url)))),\
        items(snippet(publishedAt)),items(snippet(tags))items(snippet(channelId)),\
        items(topicDetails(topicCategories)),items(snippet(categoryId))'
    )

    try:
        response = request.execute()

    except googleapiclient.errors.HttpError as e:
        # print(e.error_details[0]['reason'])
        if e.error_details[0]['reason'] == 'quotaExceeded':
            # close the current connection
            authenticated_service.close()

            try:
                # get a new set of credentials and try to activate it!
                creds = credential_paths.pop()
                authenticated_service = get_authenticated_service(creds)

                response, credential_paths, authenticated_service = get_video_info(
                    authenticated_service, id, credential_paths)

            except IndexError:
                print('Ran out of credentials! Trying again from the beginning')

                response, credential_paths, authenticated_service = get_video_info(authenticated_service, id, ['credentials/credentials1.json',
                                                                                                               'credentials/credentials2.json',
                                                                                                               'credentials/credentials3.json',
                                                                                                               'credentials/credentials4.json',
                                                                                                               'credentials/credentials5.json',
                                                                                                               'credentials/credentials6.json'])
        else:
            raise e

    finally:
        return response, credential_paths, authenticated_service


def parse_video_response(response):
    '''
    retrieves video info from a response object
    returns them individually. 
    '''
    snippet = response['items'][0]['snippet']  # gets only the snippet dict!
    topic_details = response['items'][0].get('topicDetails', pd.NA)

    category_id = snippet.get('categoryId', pd.NA)
    description = snippet.get('description', pd.NA)
    channel_id = snippet.get('channelId', pd.NA)
    published_at = snippet.get('publishedAt', pd.NA)
    thumbnail = snippet.get(
        'thumbnails', pd.NA
    ).get(
        'high', pd.NA
    ).get(
        'url', pd.NA
    )

    tag = snippet.get('tags', [])
    if tag:
        tag = ','.join(tag)
    else:
        tag = pd.NA

    if pd.isna(topic_details):
        topic_categories = pd.NA
    else:
        topic_categories = topic_details.get('topicCategories', pd.NA)

    return description, channel_id, published_at, thumbnail, tag, topic_categories, category_id


def main():
    channel_ids = []
    published_at = []
    descriptions = []
    thumbnails = []
    tags = []
    topic_categories = []
    category_ids = []
    removed_videos_ids = []

    credentials = [
        'credentials/credentials1.json',
        'credentials/credentials2.json',
        'credentials/credentials3.json',
        'credentials/credentials4.json',
        'credentials/credentials5.json',
        'credentials/credentials6.json'
    ]

    if len(sys.argv) < 2:
        raise SystemExit(f"Usage: {sys.argv[0]} <path_to_df> <path_to_enriched_df>")

    path_to_df = sys.argv[1]
    path_to_enriched_df = sys.argv[2]

    df = pd.read_csv(path_to_df, index_col=0)

    authenticated_service = get_authenticated_service(credentials[0])

    for i, id in enumerate(df.video_id):
        response, credentials, authenticated_service = get_video_info(
            authenticated_service, id, credentials)

        if response['items']:
            description, channel_id, published, thumbnail, tag, topic_category, category_id = parse_video_response(
                response)
            channel_ids.append(channel_id)
            published_at.append(published)
            descriptions.append(description)
            thumbnails.append(thumbnail)
            tags.append(tag)
            topic_categories.append(topic_category)
            category_ids.append(category_id)
        else:
            removed_videos_ids.append(id)
            print(
                f'Video number {i=} with {id=} did not have any information!')

    # fjern de id'er der ikke kan fås information på
    full_df = df[~df['video_id'].isin(removed_videos_ids)]
    # tilføj de nye lister som kolonner i en samlet df
    full_df = full_df.assign(
        channel_id=channel_ids,
        published_date=published_at,
        description=descriptions,
        thumbnail=thumbnails,
        tag=tags,
        topic_category = topic_categories,
        category_id = category_ids
    )
    full_df.to_csv(path_to_enriched_df)


if __name__ == "__main__":
    main()
