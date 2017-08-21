var dashboard = angular.module( 'dashboard', [] );

dashboard.controller( 'MainController', [ '$scope', '$timeout', function( $scope, $timeout ) {

    $scope.loggedIn = false;
    $scope.clubCode = "";
    $scope.username = "";
    $scope.password = "";
    $scope.errorLogin = false;

    $scope.softwareVer = "1.0.0.0";
    $.cookie('softwareVer', $scope.softwareVer, { path: '/' });

    if($.cookie('berpadToken') != null){
        $scope.loggedIn = true;
    } else {
        $scope.loggedIn = false;
    }

    var apiUrl = "http://api.berpad.com";
    if(location.href.indexOf('staging.berpad.com') > -1){
        apiUrl = "http://staging-api-dev.berpad.com";
    } else if(location.href.indexOf('localhost') > -1){
        apiUrl = "http://127.0.0.1:8000";
    }

    $scope.clubCodeChanged = function(clubCode){
        $scope.clubCode = clubCode;
    };
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
                $.cookie('berpadToken', response.token, { path: '/' });
                $.cookie('berpadUsername', $scope.username, { path: '/' });
                $timeout(function(){
                    $scope.clubCode = "";
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
        $.removeCookie('berpadToken', { path: '/' });
        $.removeCookie('berpadUsername', { path: '/' });
        $scope.loggedIn = false;
    }
}]);


