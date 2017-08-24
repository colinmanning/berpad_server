berpadAdmin.controller( 'MainController', [ '$scope', '$rootScope','$timeout', 'berpadService',
    function( $scope, $rootScope, $timeout, berpadService ) {

        $rootScope.token = null;
        $rootScope.username = null;
        $rootScope.softwareVer = '';

        if($.cookie('nectarToken') == null){
            window.location.replace("../../");
        } else {
            $rootScope.token = $.cookie('berpadToken');
            $rootScope.username = $.cookie('berpadUsername');
            $rootScope.softwareVer = $.cookie('softwareVer');
            berpadService.getBerpadMetadata().then(function (response) {
                $rootScope.berpadMetadata = JSON.parse(response.data);
        });
       }

        $rootScope.myIP = "";
        $.getJSON("https://api.ipify.org?format=json", function (data) {
            $rootScope.myIP = String(data.ip).split('.').join('');
        });

        $scope.backClicked = function(){
            window.location.replace("../../");
        };

        $scope.currentTab = 2;
        $scope.changeTab = function(num){
            $scope.currentTab = num;
        };

        $rootScope.selectedSportClub = null;
        $rootScope.sportClubs = [];
        $rootScope.users = [{first_name: 'test'}];
        getUsers();
        //getAllPrograms();

        function getAllSportClubs() {
            berpadService.getFilteredSportClubs('').then(function (response) {
                $rootScope.sportClubs = response.data;
            });
        };

        function getUsers() {
            berpadService.getFilteredUsers('').then(function (response) {
                $rootScope.users = response.data;
                getAllSportClubs();
            });
        };
} ] );