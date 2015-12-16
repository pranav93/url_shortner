from app import ma
from app.models import UrlInfo


class UrlInfoSchema(ma.ModelSchema):
    class Meta:
        model = UrlInfo


class UrlInfoSchemaShortUrls(UrlInfoSchema):
    class Meta:
        fields = ('tiny_url', )
