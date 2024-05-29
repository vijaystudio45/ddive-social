from django.test import TestCase

# Create your tests here.
import requests
#Your Access Keys
page_id_1 = 61554315699131
facebook_access_token_1 = 'EAAFqhDJUYBQBOZBAs5ZBRQKuzg2fbZCTdZClfeGzUeRMZANk6ZBvV417q16STTJYWQ5nIsKsQQzjC2d0eRa3XmcHL6JEdZAeihRmAoeBWgfLqAvzqZAaUdqWpFUVY9fG0sInZCXqUPJSjRqv1zFfwZBSZBr5UvyJyqVxkCXZBzkFZCsiFaqh7bNEdHj1QLagE8yZAL7zpiZBlCgDoeChmbW4dJmxryFmjCV27iyhjEmvG8ZD'
msg = 'Purple Ombre Bob Lace Wig Natural Human Hair now available on https://lace-wigs.co.za/'
post_url = 'https://graph.facebook.com/{}/feed'.format(page_id_1)
payload = {
'message': msg,
'access_token': facebook_access_token_1
}
r = requests.post(post_url, data=payload)
print(r.text)