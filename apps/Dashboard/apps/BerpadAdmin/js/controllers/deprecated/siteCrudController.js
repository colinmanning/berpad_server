backoffice.controller('SiteCrudController', ['$scope', '$timeout', 'business', 'site', '$mdDialog', '$mdToast', 'apiaryService',
    function ($scope, $timeout, business, site, $mdDialog, $mdToast, apiaryService) {

        $scope.site = angular.copy(site);
        $scope.business = business;
        $scope.tariffs = [{name:"Tariffs not available", id:-1}];

        $scope.init = function(){
            $timeout(function(){
                $('select').material_select();
            },200);
        };

        if(!$scope.site){
            resetSite();
        }
        $scope.currentTab = 1;
        $scope.title = "Edit Business Site Details";

        $scope.next = function(){
              $scope.currentTab++;
        };
        $scope.previous = function(){
              $scope.currentTab--;
        };

        $scope.saveSite = function (exit) {
            if(!$scope.site.id){
                apiaryService.createSite($scope.site).then(function(response) {
                    console.log('response.name',response.data.name);
                    $scope.business.business_sites.push(response.data);
                    $mdToast.show($mdToast.simple({position:'top right', parent:$('#mainContent')}).textContent('Site created'));
                    exitModal(exit);
                },function(error) {
                    $mdToast.show($mdToast.simple({position:'top right', parent:$('#mainContent')}).textContent('Error creating site'));
                    exitModal(exit);
                });

            } else {
                apiaryService.updateSite($scope.site).then(function(response) {
                    var siteIndx = $scope.business.business_sites.map(function(e){return e.id;}).indexOf($scope.site.id);
                    if(siteIndx > -1){
                        $scope.business.business_sites[siteIndx] = $scope.site;
                    }
                    $mdToast.show($mdToast.simple({position:'top right', parent:$('#mainContent')}).textContent('Site updated'));
                    exitModal(exit);
                },function(error) {
                    $mdToast.show($mdToast.simple({position:'top right', parent:$('#mainContent')}).textContent('Error updating site'));
                    exitModal(exit);
                });

            }
        };

        function exitModal(exit){
            if(exit){
               $mdDialog.hide();
            } else {
                resetSite();
            }
        }
        $scope.cancel = function () {
            $mdDialog.hide();
        };
        function resetSite(){
            $scope.site = {
                name:'',
                street_1: '',
                street_2: '',
                district: '',
                city: '',
                zip: '',
                country: 'US',
                state: '',
                lng: -1,
                lat: -1,
                is_hq: true,
                account_number: '',
                billing_email: '',
                billing_contact: '',
                tariff: -1,
                phone: '',
                fax: '',
                email: '',
                website: '',
                business: $scope.business.id,
                manager: $scope.business.owner,
                global_id : '',
                advisor_id: null,
                run_hours: 0
            };
        };
}]);
    