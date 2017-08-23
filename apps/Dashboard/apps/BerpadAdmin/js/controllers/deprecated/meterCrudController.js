backoffice.controller('MeterCrudController', ['$scope', '$timeout', '$mdDialog', '$mdToast', 'gateway', 'apiaryService',
    function ($scope, $timeout, $mdDialog, $mdToast, gateway, apiaryService) {

        $scope.gateway = gateway;
        $scope.meter = null;
        $scope.models = [];
        resetMeter();

        $scope.title = "Create Meter for "+ $scope.gateway.gatewayid;

        $scope.saveMeter = function (exit) {
            var ENOCEAN = "ENOCEAN-";
            $scope.meter.thingid = ENOCEAN.concat($scope.meter.pressacid);
            apiaryService.addPressac($scope.meter).then(function (response) {
                $scope.meter.id = response.data.id;
                $scope.gateway.gateway_things.push($scope.meter);
                exitModal(exit);
                $mdToast.show($mdToast.simple({position:'top right', parent:$('#mainContent')}).textContent('Meter added'));
            },function (response) {
                exitModal(exit);
                $mdToast.show($mdToast.simple({position:'top right', parent:$('#mainContent')}).textContent('Error adding meter.'));
            });
        };
        function exitModal(exit){
            if(exit){
               $mdDialog.hide();
            } else {
                resetMeter();
            }
        }
        $scope.cancel = function () {
            $mdDialog.hide();
        };
        function resetMeter(){
            $scope.meter = {
                thingid: '',
                pressacid:'',
                model: null,
                gatewayid: $scope.gateway.gatewayid,
                first_number: 1
             };
             if($scope.models.length > 0){
                $scope.meter.model = $scope.models[0];
            }
        };

        apiaryService.getApiaryMetadata().then(function (response) {
            var responseJson = JSON.parse(response.data);
            var pressac_models = responseJson.pressac_models;
            for (var property in pressac_models) {
                if (pressac_models.hasOwnProperty(property)) {
                    $scope.models.push(property);
                }
            }
            if($scope.models.length > 0){
                $scope.meter.model = $scope.models[0];
            }
        });
}]);
    