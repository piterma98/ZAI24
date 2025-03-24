import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from graphql_jwt.decorators import jwt_cookie

from api.graphql.schema import schema as user_schema

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "graphql/",
        csrf_exempt(
            jwt_cookie(
                GraphQLView.as_view(
                    schema=user_schema,
                    graphiql=settings.DEBUG,
                )
            )
        ),
        name="graphql",
    ),
    path("__debug__/", include(debug_toolbar.urls)),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
