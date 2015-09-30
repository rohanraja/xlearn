'use strict';

/**
 * @ngdoc directive
 * @name izzyposWebApp.directive:adminPosHeader
 * @description
 * # adminPosHeader
 */
angular.module('sbAdminApp')
	.directive('forkbuttons',function() {
    return {
        templateUrl:'scripts/directives/forkbuttons/forkbuttons.html',
        restrict: 'E',
        replace: true,
        scope: false,
        controller: function ($scope) {

          $scope.onForkModel = function(){

            $scope.$broadcast('fork_model');

          };

          $scope.modelStar = false;
          $scope.paramStar = false;

          $scope.$on('fork_change', function(event, mass) {
            
            if(mass[0] == "model")
              $scope.modelStar = mass[1];
            else
              $scope.paramStar = mass[1];

          });

        }
    
    }
  });
