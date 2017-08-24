backoffice.controller('MemberCrudController', ['$scope', '$timeout', 'sportclub', 'member', '$mdDialog', '$mdToast', 'berpadService',
    function ($scope, $timeout, sportclub, member, $mdDialog, $mdToast, berpadService) {

        $scope.member = angular.copy(member);
        $scope.sportclub = sportclub;

        $scope.init = function(){
            $timeout(function(){
                $('select').material_select();
            },200);
        };

        if(!$scope.member){
            resetMember();
        }
        $scope.currentTab = 1;
        $scope.title = "Edit Sport Club Member Details";

        $scope.next = function(){
              $scope.currentTab++;
        };
        $scope.previous = function(){
              $scope.currentTab--;
        };

        $scope.saveMember = function (exit) {
            if(!$scope.site.id){
                berpadService.createMember($scope.site).then(function(response) {
                    console.log('response.name',response.data.name);
                    $scope.sportclub.club_members.push(response.data);
                    $mdToast.show($mdToast.simple({position:'top right', parent:$('#mainContent')}).textContent('Member created'));
                    exitModal(exit);
                },function(error) {
                    $mdToast.show($mdToast.simple({position:'top right', parent:$('#mainContent')}).textContent('Error creating member'));
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
    