'use strict';

/**
 * @ngdoc directive
 * @name izzyposWebApp.directive:adminPosHeader
 * @description
 * # adminPosHeader
 */
angular.module('sbAdminApp')
	.directive('evaluation',function() {
    return {
        templateUrl:'scripts/directives/evaluation/evaluation.html',
        restrict: 'E',
        replace: true,
        scope: false,
        controller: function ($scope, trainerservice) {


          $scope.currentWeight = 5;
          $scope.onStartTest = function(){

            trainerservice.testSentance($scope.modelId, $scope.paramsId, $scope.sentance, $scope.currentWeight).then(function(resp){
              $scope.testResults = resp[0];
              $scope.wordResults = resp[1];
            });

            // trainerservice.testSentancePrediction($scope.modelId, $scope.paramsId, $scope.sentance, $scope.currentWeight).then(function(resp){
            //   console.log(resp);
            //   $scope.wordResults = resp;
            // });
          };


          $scope.generate_sequence = function(){
            trainerservice.generate_sequence($scope.modelId, $scope.paramsId, $scope.currentWeight).then(function(resp){
              $scope.generated_sequence = resp;
            });
          };



        }
    
    }
  });
