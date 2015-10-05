'use strict';

/**
 * @ngdoc directive
 * @name izzyposWebApp.directive:adminPosHeader
 * @description
 * # adminPosHeader
 */
angular.module('sbAdminApp')
	.directive('mapper',function() {
    return {
        templateUrl:'scripts/directives/mapper/mapper.html',
        restrict: 'E',
        replace: true,
        scope: false,
        controller: function ($scope, listservice) {


                    
          listservice.loadMappers($scope.modelId).then(function(resp){
            $scope.mappers = resp;
          });


        }
    
    }
  });
