var berpadAdmin = angular.module( 'berpadAdmin', ['ngFileUpload', 'ngMaterial', 'ngMessages'] )
    .config(function($mdThemingProvider, $mdDateLocaleProvider) {
  $mdThemingProvider.theme('default')
    .primaryPalette('green')
    .accentPalette('light-green');

      $mdDateLocaleProvider.formatDate = function(date) {
       return moment(date).format('YYYY-MM-DD');
    };
});