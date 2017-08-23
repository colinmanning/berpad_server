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
            apiaryService.getBerpadMetadata().then(function (response) {
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

        $rootScope.selectedBusiness = null;
        $rootScope.businesses = [];
        $rootScope.programs = [];
        $rootScope.users = [{first_name: 'test'}];
        getUsers();
        getAllPrograms();

        function getAllBusinesses() {
            apiaryService.getFilteredBusinesses('').then(function (response) {
                $rootScope.businesses = response.data;
            });
        };

        function getAllPrograms() {
            apiaryService.getAllPrograms().then(function (response) {
                $rootScope.programs = response.data;
            });
        };

        function getUsers() {
            apiaryService.getFilteredUsers('').then(function (response) {
                $rootScope.users = response.data;
                getAllBusinesses();
            });
        };
} ] );