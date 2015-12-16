1. Api 'url_shorten' will shorten any valid url
usage : hit 'http://localhost:5000/urls/url_shorten?url=https://www.google.co.in',
you'll get shortened url as response
response : {tiny_url: "http://localhost:5000/inflate/1"}

2. Api 'url_similar' will show the results if keyword matches either title or url string
usage : hit 'http://localhost:5000/urls/url_similar?keyword=google'
response : [
                {
                    id: 1,
                    tiny_url: "http://localhost:5000/inflate/1",
                    title: "Google",
                    url: "https://www.google.co.in",
                    url_hash: "1"
                },
                {
                    id: 2,
                    tiny_url: "http://localhost:5000/inflate/2",
                    title: "Google",
                    url: "https://www.google.com",
                    url_hash: "2"
                }
            ]

3. Api, 'inflate' will return the total number of visits and hourly visits for url shortening
usage : go to a tiny url 'http://localhost:5000/inflate/1'
response : {
                hourly_hits:
                {
                    16-12-2015T8: 15,
                    16-12-2015T9: 2
                },
                total_hits: 17
            }