var backoffice = angular.module( 'backoffice', ['ngFileUpload', 'ngMaterial', 'ngMessages'] )
    .config(function($mdThemingProvider, $mdDateLocaleProvider) {
  $mdThemingProvider.theme('default')
    .primaryPalette('green')
    .accentPalette('light-green');

      $mdDateLocaleProvider.formatDate = function(date) {
       return moment(date).format('YYYY-MM-DD');
    };
});