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
        controller: function ($scope) {

          // ToDo: Implement

          var loadSelectionList = function(){
            var out = [
              {
                id: 1,
                name: "Self Vocab"
              },
              {
                id: 2,
                name: "Cat to Numerical"
              }
              
            ]
            return out


          };

          $scope.mappers = loadSelectionList()
          ;


        }
    
    }
  });
