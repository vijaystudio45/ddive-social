import requests
import os
from openai import OpenAI
import json

OPEN_API_KEY = os.getenv('OPEN_API_KEY')
client = OpenAI(api_key=OPEN_API_KEY)

def create_linkedin_post(page_id,access_token,content):
    api_url  = 'https://api.linkedin.com/rest/posts'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Connection': 'Keep-Alive',
        'Content-Type': 'application/json',
        'LinkedIn-Version': '202402'  # Include the LinkedIn-Version header
    }
    data = {
    "author": f"urn:li:organization:{page_id}",
    "commentary": f"{content}",
    "visibility": "PUBLIC",
    "distribution": {
        "feedDistribution": "MAIN_FEED",
        "targetEntities": [],
        "thirdPartyDistributionChannels": []
    },
    "lifecycleState": "PUBLISHED",
    "isReshareDisabledByAuthor": False
    }

    response = requests.post(api_url, headers=headers, json=data)
    return response


def create_media_linkedin_post(page_id,access_token,content,media_url):
    api_url = 'https://api.linkedin.com/v2/ugcPosts'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Connection': 'Keep-Alive',
        'Content-Type': 'application/json',
        'LinkedIn-Version': '202402'  # Include the LinkedIn-Version header
    }

    post_body = {
        'author': f'urn:li:organization:{page_id}',
        'lifecycleState': 'PUBLISHED',
        'specificContent': {
            'com.linkedin.ugc.ShareContent': {
                'shareCommentary': {
                    'text': f'{content}',
                },
                'shareMediaCategory': 'ARTICLE',
                'media': [
                    {
                        'status': 'READY',
                        'description': {
                            'text': 'Read our latest blog post about LinkedIn API!',
                        },
                        'originalUrl': f'{media_url}',
                        "thumbnails": [
                            {
                                "url": f'{media_url}'
                            }
                        ],
                    },
                ],
            },
        },
        'visibility': {
            'com.linkedin.ugc.MemberNetworkVisibility': 'PUBLIC',
        },


    }

    response = requests.post(api_url, headers=headers, json=post_body)
    return response



#to post on page facebook
def create_facebook_page_post(page_id,access_token,content):
    
    post_url = 'https://graph.facebook.com/{}/feed'.format(page_id)

    payload = {
        'message': content,
        'access_token': access_token
    }

    response = requests.post(post_url, data=payload)
    return response.status_code




#image and description in one post
# def create_post_image(page_id, access_token, content, image_url=None):
#     print(image_url,'-------------------------image_url')
#     if image_url:
#         endpoint_url = "https://graph.facebook.com/me/photos"
#         data = {
#             'message': content,
#             'url': image_url,
#             'access_token': access_token
#         }
#     else:
#         endpoint_url = 'https://graph.facebook.com/{}/feed'.format(page_id)
#         data = {
#             'message': content,
#             'access_token': access_token
#         }

#     response = requests.post(endpoint_url, data=data)   
#     return response


#to post content
def create_post_fb(page_id, access_token, content):
   
    endpoint_url = 'https://graph.facebook.com/{}/feed'.format(page_id)
    data = {
        'message': content,
        'access_token': access_token
    }

    response = requests.post(endpoint_url, data=data)
    return response


# #to post and image
def create_post_image(page_id, access_token, content,image):
    endpoint_url = f"https://graph.facebook.com/me/photos"


    # Prepare the data for the API call
    data = {
        'message': content,
        'url': image,
        'access_token': access_token
    }

    # Make the POST request to Facebook Graph API
    response = requests.post(endpoint_url, data=data)
    return response


def generate_images(image_prompt):
        client = OpenAI(api_key=OPEN_API_KEY)

        response = client.images.generate(
            model="dall-e-3",
            prompt=f" Generate relevent images to {image_prompt}.",
            size="1024x1024",
            quality="standard",
            n=1,
        )

        response = response.data[0].url
        return response

def generate_facebook_post(description,company_description,categoriesdata,prompt_text, channel):

    # prompt = f"Generate {channel} post regarding {description} according to {company_description}, reference keywords {categoriesdata} and write {channel} at the end in 130 words."
    prompt = f"""Generate {channel} post of 100 words using the prompt {description} and if available, extracting relevant information from "{prompt_text}" if not available then give me relevant response.Use the {company_description} to promote in the post and create call to action in a subtle way.If you have url then show it in the post.Also use the keywords {categoriesdata} in your post."""
    print(prompt,'----------------prompt')
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=400
    )
    facebook_post = response.choices[0].text.strip()
    facebook_post = facebook_post.strip("()")
    return facebook_post

#---------------------------------fb likes and comment------------------------_#
# import requests
def facebook_likes_comments(post_id,page_access_token):

    # Graph API endpoint for getting likes and comments of a post
    url = f'https://graph.facebook.com/{post_id}?fields=likes.summary(true),comments.summary(true)&access_token={page_access_token}'

    # Send GET request to the endpoint
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        return data
        # likes_count = data['likes']['summary']['total_count']
        # comments_count = data['comments']['summary']['total_count']
        # print(f'Likes: {likes_count}, Comments: {comments_count}')
    else:
        print('Error:', response.text)



def get_shared_count(post_id,page_access_token):
    url = f'https://graph.facebook.com/v19.0/{post_id}/sharedposts'

    headers = {
        'Authorization': f'Bearer {page_access_token}'

































































        
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print(data)
        shared_posts_count = len(data.get('data', [])) 
        return shared_posts_count
        # print(f'The post has been shared {shared_posts_count} times.')
    else:
        print(f"Error: {response.status_code} - {response.text}")





# def comment_count_fb(post_id,page_access_token):

#     comments_response = requests.get(
#     f'https://graph.facebook.com/v12.0/{post_id}/comments',
#     params={'access_token': page_access_token}
# )   
#     print(comments_response)
#     response_json = json.loads(comments_response.text)
#     print(response_json,'======response_json')

#     # Get the count of comments
#     comments_count = len(response_json['data'])

#     return comments_count

#----------------------------------------------------------------------------------------------#
import requests
import io
from PIL import Image
import base64
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import default_storage


def process_image_and_save_to_model(url):
    response = requests.get(url)
    image_bytes = io.BytesIO(response.content)
    img = Image.open(image_bytes)
    jpeg_image = io.BytesIO()
    img.save(jpeg_image, format='JPEG')

    # to save file to model field
    uploaded_image = SimpleUploadedFile(
        name='generated_image.jpg',
        content=jpeg_image.getvalue(),
        content_type='image/jpeg'
    )
    return uploaded_image



def fb_upload_video(page_access_token,page_id,description,fb_video):

    url = f'https://graph-video.facebook.com/v19.0/{page_id}/videos'
    access_token = page_access_token
    file_url = fb_video
    content = description
    files = {
        'file_url': (None, file_url),
        'access_token': (None, access_token),
        'description': (None, content),
    }
    response = requests.post(url, files=files)
    print("///////////////////////////////",response.content)
    return response



#--------------------------------------instagram page/detail get---------------------------------------#

# access_token1 = "EAAZALWvsrG0oBOymaZApvrkZArCcO9M0IoIODXcpCCTMSZBeP2D3YqwU5ZCmZCETirYDhoCxfVTGpZB2AmUOx1LxMKgmqPy31ySSpAgW4liVFZAM1GjvOECNHD8dEspKkcIeQLnAnsvDe36abZCEK6APzt4lZAB1e8EiiSifAXox183H6ORtcCZBonOw0yBGKIH8mcyO44C7WGnJtxxZCjZAUOSmboO4Q4dZCbNFqKPxyWZB5I1oZC99FYmj5IXy0RhqAEJS"

def get_instagram_accounts(access_token):
    print("7777777777777777",access_token)
    url = f"https://graph.facebook.com/v19.0/me/accounts"
    params = {
        'fields': 'id,name,access_token,instagram_business_account',
        'access_token': access_token
    }

    response = requests.get(url, params=params)
    response.raise_for_status()  
    data = response.json()
    print("3333333333333333333333333",data)
    return response
    








def LinkedIn_upload_video(access_token, linkedin_page_id, file_size, upload_captions=False, upload_thumbnail=False):

   
    url = 'https://api.linkedin.com/rest/videos?action=initializeUpload'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'LinkedIn-Version': '202402'
    }
    
    # Ensure linkedin_page_id is in URN format
    linkedin_page_urn = f'urn:li:organization:{linkedin_page_id}'

    payload = {
        "initializeUploadRequest": {
            "owner": linkedin_page_urn,
            "fileSizeBytes": int(file_size),
            "uploadCaptions": upload_captions,
            "uploadThumbnail": upload_thumbnail
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print("ggggggggggggggggggiddddddddddddddddd",response.json())
    # return response
    data = response.json()
    return data['value']['video']



# def initialize_upload(access_token, linkedin_page_id, video_file_name):
#     linkedin_page_urn = f'urn:li:organization:{linkedin_page_id}'
    
#     # Get the actual file size
#     video_size_bytes = default_storage.size(video_file_name)
    
#     # Rest of the code remains the same
#     url = 'https://api.linkedin.com/v2/assets?action=registerUpload'
    
#     headers = {
#         'Authorization': f'Bearer {access_token}',
#         'Content-Type': 'application/json'
#     }
    
#     data = {
#         "registerUploadRequest": {
#             "owner": linkedin_page_urn,
#             "recipes": ["urn:li:digitalmediaRecipe:feedshare-video"],
#             "serviceRelationships": [
#                 {
#                     "relationshipType": "OWNER",
#                     "identifier": "urn:li:userGeneratedContent"
#                 }
#             ]
#         }
#     }
    
#     try:
#         # Send POST request to initialize upload
#         response = requests.post(url, headers=headers, json=data)
        
#         # Check for successful response
#         if response.status_code == 201:
#             # Extract upload URL from the response
#             upload_url = response.json().get("value", {}).get("uploadMechanism", {}).get("com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest", {}).get("uploadUrl", "")
            
#             if upload_url:
#                 # Upload the video file using the obtained upload URL
#                 with default_storage.open(video_file_name, 'rb') as video_file:
#                     upload_response = requests.put(upload_url, data=video_file)
                    
#                     if upload_response.status_code == 200:
#                         print("Video uploaded successfully!")
#                     else:
#                         print("Failed to upload video. Status code:", upload_response.status_code)
#             else:
#                 print("Failed to obtain upload URL from the response.")
#         else:
#             print("Failed to initialize upload. Status code:", response.status_code)
            
#     except requests.exceptions.RequestException as e:
#         print("Error:", e)
#         return None



def upload_video_linkedin(linkedin_data2,linkedin_page_id,access_token):
        
        print(linkedin_page_id)
        print(access_token)
        headers = {
            'Authorization': f'Bearer {access_token}',
            'X-Restli-Protocol-Version': '2.0.0',
            'LinkedIn-Version': '202402',
            'Content-Type': 'application/json'
        }

        data = {
            "author": f"urn:li:organization:{linkedin_page_id}",
            "commentary": "Sample video Post",
            "visibility": "PUBLIC",
            "distribution": {
                "feedDistribution": "MAIN_FEED",
                "targetEntities": [],
                "thirdPartyDistributionChannels": []
            },
            "media": {
                "title": "title of the video",
                "id": f"{linkedin_data2}"
            },
            "lifecycleState": "PUBLISHED",
            "isReshareDisabledByAuthor": False
        }

        print(data,'===========access_token=================')
        # Convert the data to JSON format
        json_data = json.dumps(data)

        # Make the POST request
        response = requests.post('https://api.linkedin.com/rest/posts', headers=headers, data=json_data)

        print(response.text)

        # Print the response
        return response.status_code
        



def upload_video(access_token, linkedin_page_id, file_size):
    # Step 1: Register Upload
    register_url = 'https://api.linkedin.com/v2/assets?action=registerUpload'

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    register_payload = {
        "registerUploadRequest": {
            "owner": linkedin_page_id,
            "recipes": [
                "urn:li:digitalmediaRecipe:feedshare-video"
            ],
            "serviceRelationships": [
                {
                    "relationshipType": "OWNER",
                    "identifier": "urn:li:userGeneratedContent"
                }
            ]
        }
    }

    try:
        # Register Upload
        register_response = requests.post(register_url, headers=headers, json=register_payload)
        register_response.raise_for_status()
        register_data = register_response.json()
        upload_url = register_data['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
        asset_id = register_data['value']['asset']
        
        # Step 2: Upload Video
        with open(file_size, 'rb') as video_file:
            upload_response = requests.put(upload_url, data=video_file, headers={'Authorization': f'Bearer {access_token}', 'Content-Type': 'video/mp4'})
            upload_response.raise_for_status()
            print("Video uploaded successfully!")

        # Step 3: Complete Upload
        complete_url = f"https://api.linkedin.com/v2/assets/{asset_id}/completeUpload"
        complete_payload = {}
        complete_response = requests.post(complete_url, headers=headers, json=complete_payload)
        complete_response.raise_for_status()
        print("Upload completed successfully!")

    except requests.exceptions.RequestException as e:
        print(f"Error uploading video: {e}")




import time


def post_to_instagram_story(Instagram_page_id,acces_token,description, image_url ):
  
    graph_url = 'https://graph.facebook.com/v12.0/'
    endpoint = f'{Instagram_page_id}/media'
    params = {
        'image_url': image_url,
        'caption': description,
        'access_token': acces_token
    }
    response = requests.post(f'{graph_url}{endpoint}', params=params)
    if response.status_code == 200:
        content_id = response.json().get('id')
        publish_endpoint = f'{Instagram_page_id}/media_publish'
        publish_params = {
            'creation_id': content_id,
            'access_token': acces_token
        }
        publish_response = requests.post(f'{graph_url}{publish_endpoint}', params=publish_params)
        return publish_response.json()
    else:
        return response.json()
    


from django.http import JsonResponse


def post_to_instagram_video(Instagram_page_id, access_token,description, video_url):
    # Step 1: Create the video container
    create_url = f'https://graph.facebook.com/v14.0/{Instagram_page_id}/media'
    params = {
        'media_type': 'REELS',
        'video_url': video_url,
        'caption': description,
        'access_token': access_token,
    }
    response = requests.post(create_url, params=params)
    if response.status_code != 200:
        print(f"Failed to create video container: {response.text}")
        return

    creation_id = response.json().get('id')
    if not creation_id:
        print("Creation ID not found in the response.")
        return
    print(f"Video container created with ID: {creation_id}")

    # Step 2: Poll for video processing completion
    check_status_url = f'https://graph.facebook.com/v14.0/{creation_id}?fields=status_code&access_token={access_token}'
    for _ in range(30):  # Retry up to 30 times (or 5 minutes at 10 second intervals)
        time.sleep(10)  # Wait for 10 seconds before each check
        status_response = requests.get(check_status_url)
        if status_response.status_code == 200:
            status_response_json = status_response.json()
            status_code = status_response_json.get('status_code')
            if status_code == 'FINISHED':
                print("Video processing completed.")
                break
            else:
                print("Waiting for video processing to complete...")
        else:
            print(f"Failed to check video processing status: {status_response.text}")
            return
    else:
        print("Video processing did not complete in time.")
        return

    # Step 3: Publish the video
    publish_url = f'https://graph.facebook.com/v14.0/{Instagram_page_id}/media_publish'
    publish_params = {
        'creation_id': creation_id,
        'access_token': access_token,
    }
    publish_response = requests.post(publish_url, params=publish_params)
    if publish_response.status_code == 200:
        return publish_response.json() 
        # print(f"Video published successfully: {publish_response.json()}")
    else:
        print(f"Failed to publish video: {publish_response.text}")




def upload_video_to_linkedin(access_token, linkedin_page_id, video_url,data2):
    print("778787888888888888888",video_url)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'X-Restli-Protocol-Version': '2.0.0'
    }
    
    # Step 1: Initialize an upload request
    upload_init_url = 'https://api.linkedin.com/v2/assets?action=registerUpload'
    upload_init_data = {
        "registerUploadRequest": {
            "recipes": [
                "urn:li:digitalmediaRecipe:feedshare-video"
            ],
            "owner": f'urn:li:company:{linkedin_page_id}',  # Updated owner to use company URN
            "serviceRelationships": [
                {
                    "relationshipType": "OWNER",
                    "identifier": "urn:li:userGeneratedContent"
                }
            ]
        }
    }
    try:
        response = requests.post(upload_init_url, headers=headers, json=upload_init_data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        upload_info = response.json()
        
        # Extract upload URL and asset ID from response
        upload_url = upload_info['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
        asset = upload_info['value']['asset']
        
        # Step 2: Download the video file
        file_name = os.path.basename(video_url)
        with requests.get(video_url, stream=True) as r:
            r.raise_for_status()
            with open(file_name, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        
        # Step 3: Upload the video file
        with open(file_name, 'rb') as video_file:
            upload_response = requests.put(upload_url, headers={'Authorization': f'Bearer {access_token}'}, data=video_file)
            upload_response.raise_for_status()  # Raise an exception for HTTP errors
        
        os.remove(file_name)  # Remove the downloaded file after uploading
        
        if upload_response.status_code == 201:
            print(f"Video uploaded successfully. Asset ID: {asset}")
            
            # Step 4: Create a LinkedIn post referencing the uploaded video
            create_post_url = 'https://api.linkedin.com/v2/ugcPosts'
            post_data = {
                "author": f'urn:li:company:{linkedin_page_id}',
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": data2
                        },
                        "shareMediaCategory": "VIDEO",
                        "media": [
                            {
                                "status": "READY",
                                "description": {
                                    "text": "Description of the video"
                                },
                                "media": asset,
                                "title": {
                                    "text": "Title of the Video"
                                }
                            }
                        ]
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }
            post_response = requests.post(create_post_url, headers=headers, json=post_data)
            post_response.raise_for_status()  # Raise an exception for HTTP errors
            
            if post_response.status_code == 201:
                print("Post created successfully.")
                return post_response.json() 
            else:
                print("Failed to create post.")
                print(post_response.content)
               
        else:
            print("Failed to upload video.")
            
    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err}")
    except Exception as e:
        print(f"An error occurred: {e}")

