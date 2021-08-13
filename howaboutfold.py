# tweets crawled in Aug-12-2021

'''
import tweepy

auth = tweepy.OAuthHandler('sVephMFL1y9AqWGxnVykqCMra',
                           'DlxX8SvOBlGqXVDwKlfhpSiFn3HjazejVZA9Z9ByccEdg21GSa')
auth.set_access_token('1237701684106653697-UrmyAM64V4Bne0Mr8HvaY8iJibXzDj',
                      'dVXeBXF2Y24VYJgkKpdRKki6ZjV9XN01zEgcgMF80oF4M')

api = tweepy.API(auth)


myFile = open('fold3.txt', 'w')

for tweet in tweepy.Cursor(api.search, q="Z Fold 3", lang="en", include_entities=False).items():
    if "RT" not in tweet.text:
        myFile.write(f'{tweet.text} \n')

myFile.close()
'''


from google.cloud import language_v1

myFile = open('fold3.txt', 'r')

tweets = []
lines = myFile.read().splitlines()

for line in lines:
    stripLine = line.strip()

    tweetWords = stripLine.split()
    newTweetWords = []
    for i in range(len(tweetWords)):
        if tweetWords[i][0] == '@' or tweetWords[i][0] == '#':
            continue
        newTweetWords.append(tweetWords[i])

    newString = " ".join(newTweetWords)

    if newString[:4] == 'http':
        continue
    if newString == '':
        continue

    tweets.append(newString)

myFile.close()

positiveCount = 0
negativeCount = 0
neutralCount = 0

totalSentiment = 0

# Instantiates a client
client = language_v1.LanguageServiceClient()

for i in range(len(tweets)):
    text = tweets[i]
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Detects the sentiment of the text(ignore error msg)
    sentiment = client.analyze_sentiment(
        request={'document': document}).document_sentiment
    # score: -1~0~1 = negative~neutral~positive
    score = sentiment.score

    print(f'{text}: {score}')
    totalSentiment += score

    if (score < 0):
        negativeCount += 1
    elif (score == 0):
        neutralCount += 1
    elif (score > 0):
        positiveCount += 1

print(f'positive count: {positiveCount}')
print(f'negative count: {negativeCount}')
print(f'neutral count: {neutralCount}')
print(f'total sentiment score: {totalSentiment}')

# Result

# positive count: 1184
# negative count: 218
# neutral(informational) count: 716
# total sentiment score: 274.1000031903386
# 0.1955064216764184

# Conclusion
# Initial reaction of public(on twitter) is mostly positive.
# Since it's not been long since the unpack event, there are many informative tweets too.
# Even though there are dominant quantity of positive reaction, but the quality of it is not high based on total sentiment score.
# TL;DR - positive, but not that much
