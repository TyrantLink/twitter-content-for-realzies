from requests import get,post
from requests.models import Response
from json import loads,dumps

with open('headers.json') as file: headers:dict = loads(file.read())

variables = "{\"focalTweetId\":\"twitter_id_pog\",\"with_rux_injections\":false,\"includePromotedContent\":true,\"withCommunity\":true,\"withQuickPromoteEligibilityTweetFields\":true,\"withBirdwatchNotes\":true,\"withSuperFollowsUserFields\":true,\"withDownvotePerspective\":true,\"withReactionsMetadata\":false,\"withReactionsPerspective\":false,\"withSuperFollowsTweetFields\":true,\"withVoice\":true,\"withV2Timeline\":true}"

def get_token() -> str:
	headers.pop('x-guest-token',None)
	res = post('https://api.twitter.com/1.1/guest/activate.json',headers=headers)
	return res.json()['guest_token']

def get_tweet(twitter_id) -> Response:
	res = get(
		url='https://twitter.com/i/api/graphql/WpsPNC5QMhwzpczwbXfZJQ/TweetDetail',
		params={
			"variables": variables.replace('twitter_id_pog',twitter_id),
			"features": "{\"responsive_web_graphql_timeline_navigation_enabled\":false,\"unified_cards_ad_metadata_container_dynamic_card_content_query_enabled\":true,\"tweetypie_unmention_optimization_enabled\":true,\"responsive_web_uc_gql_enabled\":true,\"vibe_api_enabled\":true,\"responsive_web_edit_tweet_api_enabled\":true,\"graphql_is_translatable_rweb_tweet_is_translatable_enabled\":false,\"standardized_nudges_misinfo\":true,\"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled\":false,\"interactive_text_enabled\":true,\"responsive_web_text_conversations_enabled\":false,\"responsive_web_enhance_cards_enabled\":true}"
		},headers=headers)
	return res

def main():
	if 'twitter.com/' not in (inp:=input('Twitter URL: ')):
		print('please enter a valid twitter.com url')
	twitter_id = inp.split('/')[-1].split('?')[0]

	res = get_tweet(twitter_id)
	if res.status_code != 200:
		headers['x-guest-token'] = get_token()
		with open('headers.json','w') as file: file.write(dumps(headers,indent=2))
		res = get_tweet(twitter_id)
	
	if res.status_code != 200:
		print(f'unable to get tweet content: status code {res.status_code}')
		return

	for entry in res.json()['data']['threaded_conversation_with_injections_v2']['instructions'][0]['entries']:
		if entry['entryId'] == f'tweet-{twitter_id}':
			print(entry['content']['itemContent']['tweet_results']['result']['legacy']['full_text'])
	
if __name__ == '__main__':
	main()