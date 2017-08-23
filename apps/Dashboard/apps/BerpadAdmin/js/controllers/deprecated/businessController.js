backoffice.controller('BusinessController', ['$scope', '$rootScope', '$mdDialog', '$timeout', 'apiaryService', '$mdToast',
    function ($scope, $rootScope, $mdDialog, $timeout, apiaryService, $mdToast) {

        $scope.searchQuery = '';
        $scope.showRecords = true;
        $scope.crudType = 'Create';

        $scope.title = "Business";
        $scope.site = null;
        $scope.noResults = false;
        
        $scope.filteredBusinesses = [];
        $scope.businessListLoading = false;
        var filterTextTimeout;

        $scope.apiaryMetadata = null;
        $scope.business_types = [];

        apiaryService.getApiaryMetadata().then(function (response) {
            $scope.apiaryMetadata = JSON.parse(response.data);
            $scope.business_types = $scope.apiaryMetadata.business_types;
            console.log('$scope.business_types',$scope.business_types);
        });

        $scope.showAll = function(){
            $scope.filteredBusinesses = [];
            if (filterTextTimeout) $timeout.cancel(filterTextTimeout);
            filterTextTimeout = $timeout(function() {
                $scope.showRecords = true;
                $scope.businessListLoading = true;
                $scope.noResults = false;
                apiaryService.getAllBusinesses().then(function (response) {
                    $scope.filteredBusinesses = response.data;
                    $scope.businessListLoading = false;
                    $scope.noResults = false;
                }).then(function (response) {
                    $scope.noResults = true;
                    $scope.businessListLoading = false;
                });
            }, 500);
        };

        $scope.searchChanged = function(query){
            $scope.filteredBusinesses = [];
            if (filterTextTimeout) $timeout.cancel(filterTextTimeout);
            filterTextTimeout = $timeout(function() {
                if(query != ''){
                    $scope.showRecords = true;
                    $scope.businessListLoading = true;
                    $scope.noResults = false;
                    apiaryService.getFilteredBusinesses(query).then(function (response) {
                        $scope.filteredBusinesses = response.data;
                        $scope.businessListLoading = false;
                        $scope.noResults = false;
                    }).then(function (response) {
                        $scope.noResults = true;
                        $scope.businessListLoading = false;
                    });
                } else {
                    $scope.noResults = false;
                }
            }, 500);
        };

        var numOfExistingSites = 0;
        $scope.selectBusiness = function (business) {
                var business_wait_load = $timeout(function() {
                                        $mdToast.show($mdToast.simple({position:'top right', parent:$('#mainContent')})
                        .textContent('Loading business ...').hideDelay(5000));

                }, 250);
                apiaryService.getBusinessComplete(business.id).then(function(response) {
                    $rootScope.selectedBusiness = response.data;
                    //$rootScope.selectedBusiness.business_type = business.business_type;
                    numOfExistingSites = $rootScope.selectedBusiness.business_sites.length;
                    $scope.searchQuery = '';
                    $scope.crudType = 'Edit';
                    $scope.showRecords = false;
                    $timeout.cancel(business_wait_load);
                    $mdToast.show($mdToast.simple({position:'top right', parent:$('#mainContent')})
                        .textContent($rootScope.selectedBusiness.name + ' business loaded.'));
                    },
                    function(response) {
                        $timeout.cancel(business_wait_load);
                         $mdToast.show($mdToast.simple({position:'top right', parent:$('#mainContent')})
                            .textContent('Failed to get business details'));
                    })

        };
        $scope.emptyBusiness  = function () {
            $rootScope.selectedBusiness = {
                name: '',
                owner: '',
                business_sites: []
            };
            $scope.showRecords = false;
            $scope.crudType = 'Create';
        };

        $scope.addSiteClicked = function(){
            var modalInstance = $mdDialog.show({
                animation: true,
                templateUrl: 'partials/modalCreateUpdateSite.html',
                controller: 'SiteCrudController',
                size: 'lg',
                backdrop: 'static',
                resolve: {
                    business: function(){ return $rootScope.selectedBusiness; },
                    site: function(){ return null; }
                }
            });
        };
        $scope.removeSiteClicked = function(site){
            alert = $mdDialog.confirm()
                .textContent("Are you sure you want to remove '" + site.name + "' site?")
                .ok('Yes')
                .cancel('No');
              $mdDialog
                  .show( alert )
                  .then(function() {
                        var siteIndx = $rootScope.selectedBusiness.business_sites.map(function(e){return e.id;}).indexOf(site.id);
                        if(siteIndx > -1){
                            $rootScope.selectedBusiness.business_sites.splice(siteIndx, 1);
                        }
                        alert = null;
                }).then(function() {
                      alert = null;
                });
        };
        $scope.editSiteClicked = function(site){
            $mdDialog.show({
                templateUrl: 'partials/modalCreateUpdateSite.html',
                controller: 'SiteCrudController',
                parent: angular.element(document.body),
                locals: {
                    business:  $rootScope.selectedBusiness,
                    site:  site
                }
            });
        };

        $scope.saveBusiness = function(){
            apiaryService.createBusiness($rootScope.selectedBusiness).then(function (response) {
                $rootScope.selectedBusiness.id = response.data.id;
                if ($rootScope.selectedBusiness.business_sites.length == 0) {
                    $rootScope.businesses.push($rootScope.selectedBusiness);
                } else {
                    numOfSitesCreated = 0;
                    for (var i = 0; i < $rootScope.selectedBusiness.business_sites.length; i++) {
                        $rootScope.selectedBusiness.business_sites[i].business = response.data.id;
                        apiaryService.createSite($rootScope.selectedBusiness.business_sites[i]).then(function (response) {
                            numOfSitesCreated++;
                            if(numOfSitesCreated == $rootScope.selectedBusiness.business_sites.length){
                                $rootScope.businesses.push($rootScope.selectedBusiness);
                                $rootScope.selectedBusiness = null;
                                numOfSitesCreated = 0;
                            }
                        });
                    }
                }
            });
            $mdToast.show($mdToast.simple({position:'top right', parent:$('#mainContent')}).textContent('Business Created'));
        };
        $scope.updateBusiness = function(){
            apiaryService.updateBusiness($rootScope.selectedBusiness).then(function (response) {
                numOfSitesCreated = 0;
                for (var i = numOfExistingSites; i < $rootScope.selectedBusiness.business_sites.length; i++) {
                    $rootScope.selectedBusiness.business_sites[i].business = response.data.id;
                    apiaryService.createSite($rootScope.selectedBusiness.business_sites[i]).then(function (response) {
                        numOfSitesCreated++;
                        if(numOfSitesCreated == $rootScope.selectedBusiness.business_sites.length){
                            $rootScope.businesses.push($rootScope.selectedBusiness);
                            $rootScope.selectedBusiness = null;
                            numOfSitesCreated = 0;
                        }
                    });
                }
                $mdToast.show($mdToast.simple({position:'top right', parent:$('#mainContent')}).textContent('Business Updated'));
            });
        };
        $scope.saveSite = function(){
            $rootScope.selectedBusiness.business_sites.push($scope.site);
            $scope.cancelSite();
        };

        $scope.doImportDI = function () {
            if ($scope.form.file.$valid && $scope.file) {
                $mdToast.show($mdToast.simple({position:'top right', parent:$('#mainContent')}).textContent('DI File Import Started'));
                apiaryService.importDI($rootScope.selectedBusiness.id, $scope.file)
                    .then(function (response) {
                        console.log('Success ' + response.config.data.file.name + 'uploaded.');
                        $timeout(function(){
                            $scope.selectBusiness($rootScope.selectedBusiness);
                            $mdToast.show($mdToast.simple({position:'top right', parent:$('#mainContent')}).textContent('DI File Imported'));
                        });
                    }, function (response) {
                        console.log('Error status: ' + response.status);
                        $mdToast.show($mdToast.simple({position:'top right', parent:$('#mainContent')}).textContent('DI File Import failed'));
                    }, function (evt) {
                        var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
                        console.log('progress: ' + progressPercentage + '% ' + evt.config.data.file.name);
                    })
            }
        };

    }]);