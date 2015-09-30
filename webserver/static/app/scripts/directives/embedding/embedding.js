'use strict';

/**
 * @ngdoc directive
 * @name izzyposWebApp.directive:adminPosHeader
 * @description
 * # adminPosHeader
 */
angular.module('sbAdminApp')
	.directive('embedding',function() {
    return {
        templateUrl:'scripts/directives/embedding/embedding.html',
        restrict: 'E',
        replace: true,
        scope: false,
        controller: function ($scope) {

          // ToDo: Implement

          var loadSelectionList = function(){

            var out = [
              {
                id: 0,
                name: "Gaussian"
              },
              {
                id: 2,
                name: "Word2Vec"
              }
              
            ];

            return out;

          };


          $scope.embeddings = loadSelectionList();


        }
    
    }
  });
