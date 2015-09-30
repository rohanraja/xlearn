'use strict';

/**
 * @ngdoc directive
 * @name izzyposWebApp.directive:adminPosHeader
 * @description
 * # adminPosHeader
 */
angular.module('sbAdminApp')
	.directive('model',function() {
    return {
        templateUrl:'scripts/directives/model/model.html',
        restrict: 'E',
        replace: true,
        scope: false,
        controller: function ($scope) {

          // ToDo: Implement

          var loadSelectionList = function(){
            var out = [
              {
                id: 0,
                name: "RNN"
              },
              {
                id: 2,
                name: "LSTM"
              }
              
            ]
            return out


          };

          $scope.models = loadSelectionList()
          ;


        }
    
    }
  });
