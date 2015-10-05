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
        controller: function ($scope, listservice) {


          listservice.loadModels($scope.modelId).then(function(resp){
            $scope.models = resp;
          });


        }
    
    }
  });
