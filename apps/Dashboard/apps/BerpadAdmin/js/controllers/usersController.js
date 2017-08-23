berpadAdmin.controller('UsersController', ['$scope', '$rootScope', '$timeout', 'berpadService', '$mdToast',
    function ($scope, $rootScope, $timeout, berpadService, $mdToast) {

        $scope.searchQuery = '';
        $scope.crudType = 'Create';
        $scope.selectedUser = null;
        $scope.roles = [];
        getAllRoles();
        $scope.sites = [];
        $scope.defaultSites = [];
        getAllSites();

        $scope.filteredUsers = [];
        $scope.userListLoading = false;
        var filterTextTimeout;
        var filterSiteTextTimeout;

        $scope.showAll = function(){
            $scope.showRecords = true;
            $scope.filteredUsers = [];
            $scope.selectedUser = null;
            if (filterTextTimeout) $timeout.cancel(filterTextTimeout);
            filterTextTimeout = $timeout(function() {
                $scope.userListLoading = true;
                apiaryService.getAllUsers().then(function (response) {
                    $scope.filteredUsers = filterResults(response.data);
                    $scope.userListLoading = false;
                });
            }, 500);
        };
        $scope.searchChanged = function(query){
            $scope.filteredUsers = [];
            if (filterTextTimeout) $timeout.cancel(filterTextTimeout);
            filterTextTimeout = $timeout(function() {
                if(query != ''){
                    $scope.showRecords = true;
                    $scope.userListLoading = true;
                    $scope.selectedUser = null;
                    apiaryService.getFilteredUsers(query).then(function (response) {
                        $scope.filteredUsers = filterResults(response.data);
                        $scope.userListLoading = false;
                    });
                }
            }, 500);
        };
        function filterResults(response){
            var temArray = [];
            for(var i = 0; i < response.length; i++){
                if (response[i].business == $rootScope.selectedBusiness.id ){
                    temArray.push(response[i]);
                }
            }
            if(temArray.length == 0){
                $scope.noResults = true;
            } else {
                $scope.noResults = false;
            }
            return temArray;
        };


        $scope.selectUser = function (person) {
            $scope.userListLoading = true;
            $scope.selectedUser = person;
            apiaryService.getUserById(person.user).then(function (response) {
                for (var attrname in response.data) {
                    if(attrname != "id"){
                        $scope.selectedUser[attrname] = response.data[attrname];
                    }
                }
                console.log('$scope.selectedUser',$scope.selectedUser);
                $scope.userListLoading = false;
            });

            $scope.searchQuery = '';
            $scope.crudType = 'Edit';
            $scope.showRecords = false;
        };
        $scope.emptyUser = function () {
            $scope.selectedUser = {
                first_name: '',
                last_name: '',
                email: '',
                username: '',
                password: '',
                business: $rootScope.selectedBusiness.id,
                sites: [],
                role: [],
                default_site: null
            };
            $scope.showRecords = false;
            $scope.crudType = 'Create';
        };
        $scope.createUser = function () {
            apiaryService.createPerson($scope.selectedUser).then(function (response) {
                if(response.data.data.id){
                    $scope.selectedUser.user = response.data.data.id;
                }
                $mdToast.show($mdToast.simple({position:'top right', parent:$('#mainContent')}).textContent(response.data.message));
            });
        };
        $scope.updateUser = function () {
            console.log(JSON.stringify($scope.selectedUser));
            apiaryService.updateUser($scope.selectedUser).then(function (response) {
                apiaryService.updatePerson($scope.selectedUser).then(function (response) {
                    $mdToast.show($mdToast.simple({position:'top right', parent:$('#mainContent')}).textContent('User Updated'));
                },function (response) {
                    $mdToast.show($mdToast.simple({position:'top right', parent:$('#mainContent')}).textContent('User updating failed'));
                });
            });
        };

        function getAllRoles() {
            apiaryService.getRoles().then(function (response) {
                $scope.roles = response.data;
            });
        };
        function getAllSites() {
            apiaryService.getFilteredSites('').then(function (response) {
                $scope.sites = response.data;
            });
        };
        $scope.siteListChanged = function(){
            $scope.defaultSites = [];
            for(var i=0; i< $scope.selectedUser.sites.length; i++){
                var indx = $rootScope.selectedBusiness.business_sites.map(function(e){return e.id;})
                    .indexOf($scope.selectedUser.sites[i]);
                $scope.defaultSites.push($rootScope.selectedBusiness.business_sites[indx]);
            }
        };
    }]);