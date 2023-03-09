import api

startDate = "2020-01-01"
endDate = "2020-01-03"
timeUnit = 'date'
device = ''
ages = []
gender = ''

keyword_group_set = {
    'keyword_group_1': {'groupName': "애플", 'keywords': ["애플","Apple","AAPL"]},
    'keyword_group_2': {'groupName': "아마존", 'keywords': ["아마존","Amazon","AMZN"]},
    'keyword_group_3': {'groupName': "구글", 'keywords': ["구글","Google","GOOGL"]},
    'keyword_group_4': {'groupName': "테슬라", 'keywords': ["테슬라","Tesla","TSLA"]},
    'keyword_group_5': {'groupName': "페이스북", 'keywords': ["페이스북","Facebook","FB"]}
}


search = api.NaverSearchAPI()
search.add_keyword_group(keyword_group_set['keyword_group_1'])
search.add_keyword_group(keyword_group_set['keyword_group_2'])
search.add_keyword_group(keyword_group_set['keyword_group_3'])

search_df = search.get_data(startDate, endDate, timeUnit, ages, gender, device)
print(search_df)
