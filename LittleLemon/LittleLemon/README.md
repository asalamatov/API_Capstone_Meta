# Token-based authentication in DRF

1. project > settings.py > INSTALLED_APPS > 'rest_framework.authtoken'
2. $ pipenv shell
3. $ python manage.py makemigrations + migrate
4. $ python manage.py createsuperuser
5. http://localhost:8000/admin > Tokens > Add > choose admin > SAVE > copy KEY
6. app > views.py > 
    from rest_framework.decorators import api_view
    from rest_framework.response import Response
    @api_view()
    def secret(request):
        return Response({"message" : "Some secret message"})
7. app > urls.py > urlpatterns > 
    path("secret/", views.secret)
8. http://localhost:8000/secret/ > "# Not secret at all"
9. views.py > 
    from rest_framework.permissions import IsAuthenticated
    from rest_framework.decorators import permission_classes
10. view.py > (add to step 6 ) > 
    @api_view()
    @permission_classes([IsAuthenticated])
    def secret(request):
        return Response({"message" : "Some secret message"})
11. insomnia > GET >
    http://localhost:8000/secret/ >  # no permission
12. setting.py > REST_FRAMEWORK > 
    'DEFAULT_AUTHENTICATION_CLASSES' : (
        'rest_framework.authentication.TokenAuthentication',
    )
13. http://localhost:8000/admin > copy API-KEY
14. insomnia > Auth > Bearer Token > 
    `Token`  >>> API-KEY
    `Prefix` >>> Token
    SEND
    >
    message: Some secret message
15. app > urls.py > 
    from rest_framework.authtoken.views import obtain_auth_token > urlpatterns >
    path('api-token-auth/', obtain_auth_token)  # only HTTP POST calls
16. http://localhost:8000/api/api-token-auth/ > POST > SEND > no permission >
    Form > 
    `username` >>> admin
    `password` >>> password 
    > 
    token : API-KEY

*******************************************************************************************
# User Roles : Authorization
1. admin panel > add group Manager (do not select permissions) > SAVE
2. create users > johndoe: Manager, jimmydoe: User
3. views.py > manager_view (similar to secret view) > add to app's urls.py
4. insomnia > http://localhost:8000/api/api-token-auth/ > POST > Form > username/password : John Doe > SEND > save token
5. insomnia > http://localhost:8000/api/api-token-auth/ > POST > Form > username/password :Jimmy Doe > SEND > save token
6. insomnia > http://localhost:8000/api/manager-view/ > GET > Bearer > token > SEND > see only manager message (simple users can also see it)
7. views.py > 
    @api_view()
    @permission_classes([IsAuthenticated])
    def manager_view(request):
        if request.user.groups.filter(name="Manager").exists():
            return Response({"message": "Only Manager can see this"})
        else:
            return Response({'message': "You are not authorized"}, 403)

********************************************************************************************
# Throttling
1. views.py > urls.py(app)
    from rest_framework import AnonRateThrottle, UserRateThrottle
    from rest_framework.decorators import throttle_classes
    @api_view()
    @throttle_classes([AnonRatThrottle])
    def throttle_check(request):
        return Response({"message": "successful"})

    @api_view()
    @permission_classes([IsAuthenticated])
    @throttle_classes([UserRateThrottle])
    def throttle_check_auth(request):
        return Response({"message": "message for the logged in users only"})


2. settings.py > 
    REST_FRAMEWORK = {
        'DEFAULT_THROTTLE_RATES': {
            'anon' : "20/day",
            'user' : '5/minute',
            'ten'  : '10/minute'
        }
    }
3. check the api in insomnia or website
4. throttles.py > 
    from rest_framework.throttling import UserRateThrottle
    class TenCallPerMinute(UserRateThrottle):
        scope = 'ten'
5. step 2 last line
6. views.py
    from .throttles import TenCallsPerMinute
    @api_view()
    @permission_classes([IsAuthenticated])
    @throttle_classes([TenCallPerMinute])
    def throttle_check_auth(request):
        return Response({"message": "message for the logged in users only"})
****************************************************************************************
# Djoser
1. pipenv shell > pipenv install djoser
2. settings.py > INSTALLED_APPS > add 'djoser' after 'rest_framework'
3. settings.py >
    DJOSER = {
        'USER_ID_FIELD' : 'username'     #, 
        # 'LOGIN_FIELD' : 'email'
    }
4. settins.py > if using authentication classes together with djoser: 
    add 'rest_framework.authentication.SessionAuthentification' > 
    REST_FRAMEWORK = {
        'DEFAULT_RENDERER_CLASSES': [
            'rest_framework.renderers.JSONRenderer',
            'rest_framework.renderers.BrowsableAPIRenderer',
        ],
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.TokenAuthentication',
            'rest_framework.authentication.SessionAuthentification', ####################
        ),
        'DEFAULT_THROTTLE_RATES': {
            'anon' : "20/day",
            'user' : '5/minute',
            'ten'  : '10/minute'
        },
        'DEFAULT_THROTTLE_CLASSES': [
            'rest_framework.throttling.AnonRateThrottle',
            'rest_framework.throttling.UserRateThrottle',
        ]
    }
5. project > urls.py >
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('api/', include('LittleLemonAPI.urls')),
        path('auth/', include('djoser.urls')),
        path('auth/', include('djoser.urls')),
    ]
6. djoser supports following: 
    http:/127.0.0.1:8000/auth + 
        /users/
        /users/me/
        /users/confirm/
        /users/resend_activation/
        /users/set_password/
        /users/reset_password/
        /users/reset_password_confirm/
        /users/set_username/
        /users/reset_username/
        /users/reset_username_confirm/
        /token/login/
        /token/logout/
*******************************************************************************
# JWT - JSON Web Token
1. pipenv shell
2. pipenv install djangorestframework-simplejwt~=5.2.1
3. settings.py > INSTALLED_APPS > 'rest_framework_simplejwt', > 
    REST_FRAMEWORK = {
        'DEFAULT_RENDERER_CLASSES': [
            'rest_framework.renderers.JSONRenderer',
            'rest_framework.renderers.BrowsableAPIRenderer',
        ],
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework_simplejwt.authentication.JWTAuthentication', ############################
            'rest_framework.authentication.TokenAuthentication',
            'rest_framework.authentication.SessionAuthentication',
        ),
        'DEFAULT_THROTTLE_RATES': {
            'anon' : "20/day",
            'user' : '5/minute',
            'ten'  : '10/minute'
        },
        'DEFAULT_THROTTLE_CLASSES': [
            'rest_framework.throttling.AnonRateThrottle',
            'rest_framework.throttling.UserRateThrottle',
        ]
    }
4. project > urls.py > 
    from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView >
    path('api/token/', TokenObtainPairView.as_view(), name = 'token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name = 'token_refresh'),
5. insomnia > POST > http://localhost:8000/api/token/ > FORM (username/password) >
    * access token > expires in 5 mins > authenticate api calls
    * refresh token > regenerate access token
6. setting.py >
    SIMPLE_JWT = {
        'ACCESS_TOKEN_LIFETIME' : timedelta(minutes=5) # the shorter - the better
    }
7. copy access token > Insomnia > GET > http://localhost:8000/api/secret > Bearer Token > access token (no prefix) > SEND > message
8. after 5 mins > expires > POST > http://localhost:8000/api/token/refresh/ > FORM > refresh : (refresh token) > receive access token
9. blacklist : settings.py > INSTALLED_APPS > 'rest_framework_simplejwt.token_blacklist',
10. python manage.py migrate > runserver
11. project > urls.py > 
    from rest_framework_simplejwt.views import TokenBlacklistView
11. project > urls.py > urlpatterns += 
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
12. Insomnia > http://localhost:8000/api/token/blacklist/ > POST > FORM > refresh : (refresh token) > SEND > {} > (now you cannot use this token to regenerate access token)

****************************************************************************************************
# User Account Management 
1. Insomnia > http://localhost:8000/auth/users/ > POST > FORM (username/email/password) > user created
2. views.py > 
    from rest_framework.permissions  import IsAdminUser
    @api_view(["POST"])
    @permission_classes([IsAdminUser])
    def managers(request):
        return Response({"message": "ok"})
3. urls.py (app) ex: (/groups/manager/users)
4. insomnia > POST > http://localhost:8000/api/groups/manager/users/ > Bearer Token of Admin > see message OK
5. views.py > 
    from django.contrib.auth.models import User, Group
    @api_view(["POST", "DELETE"])
    @permission_classes([IsAdminUser])
    def managers(request):
        username = request.data['username']
        if username :
            user = get_object_or_404(User, username = username)
            managers = Group.objects.get(name="Manager")
            if request.method == "POST":
                managers.user_set.add(user)
            elif request.method == "DELETE":
                managers.user_set.remove(user)
            return Response({"message": "ok"})
        return Response({"message": "error"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "ok"})

