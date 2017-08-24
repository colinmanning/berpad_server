backoffice.factory( 'berpadService', ['$rootScope', '$http','Upload',
    function ($rootScope, $http, Upload) {

    var factory = {};

    var apiUrl = "http://api.berpad.com";
    if(location.href.indexOf('staging.berpad.com') > -1){
        apiUrl = "http://staging-api-dev.berpad.com";
    } else if(location.href.indexOf('localhost') > -1){
        apiUrl = "http://127.0.0.1:8000";
    }


    // Colin testing
    //apiUrl = "https://apiary-api-dev.lime-energy.com";

    factory.metatata = undefined;

    factory.getAllUsers = function() {
        return $http({
            method: 'GET',
            url: apiUrl + "/persons/",
            responseType:'json',
            headers: {'Authorization': 'Token '+ $rootScope.token}
        });
    };
    factory.getUserById = function(userId) {
        return $http({
            method: 'GET',
            url: apiUrl + "/users/"+userId+"/",
            responseType:'json',
            headers: {'Authorization': 'Token '+ $rootScope.token}
        });
    };

    factory.getFilteredUsers = function(filter) {
        return $http({
            method: 'GET',
            url: apiUrl + "/persons/?search="+filter,
            responseType:'json',
            headers: {'Authorization': 'Token '+ $rootScope.token}
        });
    };
    factory.updateUser = function(user) {
        var userData = {
            id: user.user,
            first_name: user.first_name,
            last_name: user.last_name,
            email: user.email,
            username: user.username
        };
        return $http({
            method: 'PUT',
            url: apiUrl + "/users/"+user.user+"/",
            data: userData,
            responseType:'json',
            headers: {'Authorization': 'Token '+ $rootScope.token}
        });
    };
    factory.createUser = function(user) {
        return $http({
            method: 'POST',
            url: apiUrl + "/users/",
            data: user,
            responseType:'json',
            headers: {'Authorization': 'Token '+ $rootScope.token}
        });
    };
    factory.createPerson = function(user) {
        return $http({
            method: 'POST',
            url: apiUrl + "/persons/create_person/",
            data: user,
            responseType:'json',
            headers: {'Authorization': 'Token '+ $rootScope.token}
        });
    };
    factory.updatePerson = function(user) {
        return $http({
            method: 'PUT',
            url: apiUrl + "/persons/"+user.username+"/",
            data: user,
            responseType:'json',
            headers: {'Authorization': 'Token '+ $rootScope.token}
        });
    };
    factory.getFilteredSites= function(filter) {
        return $http({
            method: 'GET',
            url: apiUrl + "/sites/?search="+filter,
            responseType:'json',
            headers: {'Authorization': 'Token '+ $rootScope.token}
        });
    };
    factory.createClub = function(club) {
        return $http({
            method: 'POST',
            url: apiUrl + "/clubs/",
            data: club,
            responseType:'json',
            headers: {'Authorization': 'Token '+ $rootScope.token}
        });
    };
    factory.updateClub = function(club) {
        return $http({
            method: 'PUT',
            url: apiUrl + "/clubs/"+club.id+"/",
            data: club,
            responseType:'json',
            headers: {'Authorization': 'Token '+ $rootScope.token}
        });
    };
    factory.removeClub = function(club) {
        return $http({
            method: 'DELETE',
            url: apiUrl + "/clubs/"+club.id+"/",
            responseType:'json',
            headers: {'Authorization': 'Token '+ $rootScope.token}
        });
    };

    factory.createSportClub = function(sport_club) {
        return $http({
            method: 'POST',
            url: apiUrl + "/sportclubs/",
            data: sport_club,
            responseType:'json',
            headers: {'Authorization': 'Token '+ $rootScope.token}
        });
    };
    factory.updateSportClub = function(sport_club) {
        return $http({
            method: 'PUT',
            url: apiUrl + "/sportclubs/"+sport_club.id+"/",
            data: club,
            responseType:'json',
            headers: {'Authorization': 'Token '+ $rootScope.token}
        });
    };
    factory.removeSportClub = function(sport_club) {
        return $http({
            method: 'DELETE',
            url: apiUrl + "/sportclubs/"+sport_club.id+"/",
            responseType:'json',
            headers: {'Authorization': 'Token '+ $rootScope.token}
        });
    };

    factory.getAllClubs = function() {
        return $http({
            method: 'GET',
            url: apiUrl + "/clubs/",
            responseType:'json',
            headers: {'Authorization': 'Token '+ $rootScope.token}
        });
    };

    factory.getRoles= function() {
        return $http({
            method: 'GET',
            url: apiUrl + "/roles/",
            responseType:'json',
            headers: {'Authorization': 'Token '+ $rootScope.token}
        });
    };

    factory.getBerpadMetadata = function() {
        return $http({
            method: 'GET',
            url: apiUrl + "/berpad/metadata/",
            responseType:'application/json',
            headers: {'Authorization': 'Token '+ $rootScope.token}
        });
    };


    factory.getClubComplete = function(club_id) {
        console.log('club_id', club_id);
        var getUrl = apiUrl +  "/club_id/" + club_id.toString() + "/complete_details/";
        return $http({
            method: 'GET',
            url: getUrl,
            responseType:'json',
            headers: {'Authorization': 'Token '+ $rootScope.token}
        });
    };

    factory.generateMembershipForm = function(proposal) {
        return $http({
            method: 'GET',
            url: apiUrl + "/proposals/"+proposal.id+"/generate_pdf/?email_to=colin@berpad.com",
            responseType:'application/json',
            headers: {'Authorization': 'Token '+ $rootScope.token}
        })
    };

    factory.getClubPersons = function(club_id) {
        return $http({
            method: 'GET',
            url: apiUrl +  + "/clubs/" + club_id.toString() + "/persons/",
            responseType:'json',
            headers: {'Authorization': 'Token '+ $rootScope.token}
        });
    };

    factory.getRolePersons = function(role_name) {
        return $http({
            method: 'GET',
            url: apiUrl + "/persons/for_role/?name=" + role_name,
            responseType:'json',
            headers: {'Authorization': 'Token '+ $rootScope.token}
        });
    };

    return factory;
}]);