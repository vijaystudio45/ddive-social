import requests
from django.http import JsonResponse

# def get_instagram_metrics(request):
#     # Your access token
#     access_token = 'EAAZALWvsrG0oBOymaZApvrkZArCcO9M0IoIODXcpCCTMSZBeP2D3YqwU5ZCmZCETirYDhoCxfVTGpZB2AmUOx1LxMKgmqPy31ySSpAgW4liVFZAM1GjvOECNHD8dEspKkcIeQLnAnsvDe36abZCEK6APzt4lZAB1e8EiiSifAXox183H6ORtcCZBonOw0yBGKIH8mcyO44C7WGnJtxxZCjZAUOSmboO4Q4dZCbNFqKPxyWZB5I1oZC99FYmj5IXy0RhqAEJS'
#     # The media ID you want to get metrics for
#     media_id = '18053549602604789'
    
#     # The metrics we want to fetch
#     metrics = 'like_count,comments_count'
#     # Building the URL for the request
#     url = f'https://graph.instagram.com/v14.0/{media_id}?fields={metrics}&access_token={access_token}'

#     try:
#         # Sending the GET request to the Instagram Graph API
#         response = requests.get(url)
#         print("gtrrrrsfsfsfsfsf",response)
#         # Parsing the response to JSON
#         data = response.json()

#         # Extracting the metrics
#         likes = data.get('like_count', 0)
#         comments = data.get('comments_count', 0)
#         # Instagram Graph API does not directly provide shares count, this is an example placeholder
#         shares = 'Not directly available'
#         print("frrrrrrrrrrrrrrrr",likes)
#         print("oooooooooooooo",comments)
#         # Returning the metrics as JSON
#         return JsonResponse({'likes': likes, 'comments': comments, 'shares': shares})
#     except Exception as e:
#         # If something went wrong, return an error message
#         return JsonResponse({'error': str(e)})
    # 18064651372519403





def get_post_share_count(api_version, user_id, access_token, start_timestamp, end_timestamp):
    
    # Define the endpoint URL
    url = f"https://graph.facebook.com/{api_version}/{user_id}/insights"

    # Define the parameters
    params = {
        "metric": "shares",
        "period": "day",
        "metric_type": "total_value",
        "since": start_timestamp,
        "until": end_timestamp,
        "access_token": access_token
    }

    # Make the GET request
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        share_count = data['data'][0]['values'][0]['value']
        return share_count
    else:
        print("Failed to retrieve share count:", response.text)
        return None

api_version = "v19.0"  # Update with the appropriate API version
user_id = 17910641192929094
access_token = "EAAZALWvsrG0oBO79ZA9CSA2BFjoMZBGXuEzlJabjxPamm39bIJBsgHQwm4ZALfOyBLoY5q7eJBiQM0ZA4e3fBPZBmuG1ZC8uw2K4fAHHMGP0Tr45ZBg3szGxryXDTigtJEGlG1miFf5Ja6ouwryxKmirSBiUpaPy8E0WGMkEY6JZArouWmbe25ea7uv8K73nPnelT6hcxoalQdKzV3PKiEMX6ZC4oSHCG79CAw6EvrNS3oQpWTWXoLPmO1k6CvwZCP4"
start_timestamp = 1649256000
end_timestamp = 1649342399

share_count = get_post_share_count(api_version, user_id, access_token, start_timestamp, end_timestamp)
if share_count is not None:
    print("Share count:", share_count)    