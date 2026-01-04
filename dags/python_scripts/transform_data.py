import logging
def organise_data(data):
    ''' This function will organise the api response into the below schema
        id : integer, ->primary key
        title: string,
        url: string,
        timestamp: string,
        summary: string,
        source: string,
        category: string,
        topics: dict,
        overall_sentiment_score: float,
        overall_sentiment_label: string,
        ticker_sentiment: dict
    '''
    cleaned_data = []

    numberOfRecords = int(data['items'])
    if numberOfRecords>0:

        for record in range(0,numberOfRecords):
            cleaned_data.append(
            {
            "id" : record,
            "title": str(data['feed'][record]['title']),
            "url" : data['feed'][record]['url'],
            "timestamp": data['feed'][record]['time_published'],
            "summary" : str(data['feed'][record]['summary']),
            "source" : str(data['feed'][record]['source']),
            "category" : str(data['feed'][record]['category_within_source']),
            "topics" : data['feed'][record]['topics'],
            "overall_sentiment_score" : float(data['feed'][record]['overall_sentiment_score']),
            "overall_sentiment_label" : str(data['feed'][record]['overall_sentiment_label']),
            "ticker_sentiment" : data['feed'][record]['ticker_sentiment']
            }
        )
    else:
        logging.error("number of records is less than 0")
    return cleaned_data