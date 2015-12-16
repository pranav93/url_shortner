from urlparse import urlparse, urlunparse
from flask_restful import Resource, reqparse
from lxml.html import parse
from urllib2 import URLError, urlopen
from sqlalchemy import or_

from app import api, db
from app.models import UrlInfo, UrlHits
from convert_base_62.base62 import Base62
from app.schema import UrlInfoSchema, UrlInfoSchemaShortUrls
from app.config import tiny_url


class UrlShorten(Resource):

    def get(self):
        """
        It registers a visit for a url and returns the shortened url
        :return: tiny url
        """
        parser = reqparse.RequestParser()
        parser.add_argument('url', type=str)
        url = parser.parse_args().get('url')

        if url is None:
            return {'error': 'Please provide a url with params ?url=some_url'}, 422

        url_in_db = UrlInfo.query.filter_by(url=url).first()

        # if there is no url then create a new one
        if not getattr(url_in_db, 'url_hash', None):
            try:
                title = self.get_title(url=url)
            except ValueError:
                # return the url if invalid
                return {'error': 'invalid url : ' + url}

            # add the url in db
            url_in_db = UrlInfo(url=url, title=title)
            db.session.add(url_in_db)
            db.session.commit()

            # calculate the hash 62 and update it in db
            url_hash = Base62().encode(url_id=url_in_db.id)
            url_in_db.url_hash = url_hash
            url_in_db.tiny_url = tiny_url + url_hash
            db.session.commit()

        # add the visit to url_hits table
        url_hits = UrlHits(url_hash=url_in_db.url_hash)
        db.session.add(url_hits)
        db.session.commit()

        url_info_schema = UrlInfoSchemaShortUrls()
        return url_info_schema.dump(url_in_db).data

    def get_title(self, url):
        """
        This method gets the title for url.
        :param url: url to be visited to get title
        :return: title
        """
        try:
            scheme, netloc, path, params, query, fragment = urlparse(url)
            if not netloc:
                scheme, netloc, path = 'http', path, ''
                url = urlunparse((scheme, netloc, path, params, query, fragment))
            print url
            response = urlopen(url)
            return parse(response).find('.//title').text
        except URLError:
            return 'NA'


class UrlSimilar(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('keyword', type=str)
        keyword = parser.parse_args().get('keyword')
        if keyword is None:
            return {'error': 'Please provide a url with params ?keyword=some_keyword'}, 422
        all_urls = UrlInfo.query.filter(
            or_(UrlInfo.url.like('%' + keyword + '%'), UrlInfo.title.like('%' + keyword + '%'))).all()
        url_info_schema = UrlInfoSchema()
        return [url_info_schema.dump(a_url).data for a_url in all_urls]


class Inflate(Resource):

    def get(self, url_hash):
        id = Base62().decode(url_hash=url_hash)
        url_in_db = UrlInfo.query.filter_by(id=id).first()

        if not url_in_db:
            return 'not valid url'
        else:
            response = {}
            hourly_hits = {}
            # raw mysql query to get hourly info
            result = db.engine.execute(
                "SELECT DAY(visit_time), MONTH(visit_time), YEAR(visit_time), HOUR(visit_time), COUNT(*) " +
                "FROM url_hits WHERE url_hash=%s GROUP BY HOUR(visit_time)" % url_in_db.url_hash)
            total_hits = 0
            for row in result:
                hourly_hits.update({
                    '-'.join(map(str, row[0:3])) + 'T' + str(row[3]): row[4]
                })
                total_hits += row[4]

            return response.update({'total_hits': total_hits}) or response.update({'hourly_hits': hourly_hits})\
                   or response


api.add_resource(UrlShorten, '/urls/url_shorten', endpoint='url_shorten')
api.add_resource(UrlSimilar, '/urls/url_similar', endpoint='url_similar')
api.add_resource(Inflate, '/inflate/<string:url_hash>', endpoint='inflate')