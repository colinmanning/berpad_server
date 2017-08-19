var dashboard = angular.module( 'dashboard', [] );

dashboard.controller( 'MainController', [ '$scope', '$timeout', function( $scope, $timeout ) {

    $scope.loggedIn = false;
    $scope.username = "";
    $scope.password = "";
    $scope.errorLogin = false;

    $scope.softwareVer = "1.10.15";
    $.cookie('softwareVer', $scope.softwareVer, { path: '/' });

    if($.cookie('nectarToken') != null){
        $scope.loggedIn = true;
    } else {
        $scope.loggedIn = false;
    }

    var apiUrl = "http://api.nectar.resourcekraft.com";
    if(location.href.indexOf('apiary.lime-energy.com') > -1){
        apiUrl = "https://apiary-api-dev.lime-energy.com";
    } else if(location.href.indexOf('localhost') > -1){
        apiUrl = "http://127.0.0.1:8000";
    }

    $scope.usernameChanged = function(username){
        $scope.username = username;
    };
    $scope.passwordChanged = function(password){
        $scope.password = password;
    };

    $scope.loginClicked = function(){
        $.ajax({
            url: apiUrl + "/api-token-auth/",
            type: 'POST',
            data:{
                username: $scope.username,
                password: $scope.password
            },
            success: function(response) {
                $.cookie('nectarToken', response.token, { path: '/' });
                $.cookie('nectarUsername', $scope.username, { path: '/' });
                $timeout(function(){
                    $scope.username = "";
                    $scope.password = "";
                    $scope.loggedIn = true;
                });
            },
            error: function() {
                $timeout(function(){
                    $scope.errorLogin = true;
                });
            }
        });
    };
    $scope.menuClicked = function(appName){
        if(appName == 'testin'){
            window.location.replace("apps/TestInTool");
        } else if(appName == 'backoffice'){
            window.location.replace("apps/BackOffice");
        } else if(appName == 'canary2'){
            window.location.replace("apps/Canary2web/admin/templates/admin.jinja2.html");
        }
    };
    $scope.logoutClicked = function(){
        $.removeCookie('nectarToken', { path: '/' });
        $.removeCookie('nectarUsername', { path: '/' });
        $scope.loggedIn = false;
    }
}]);


