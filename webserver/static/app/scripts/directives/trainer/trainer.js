'use strict';

/**
 * @ngdoc directive
 * @name izzyposWebApp.directive:adminPosHeader
 * @description
 * # adminPosHeader
 */
angular.module('sbAdminApp')
	.directive('trainer',function() {
    return {
        templateUrl:'scripts/directives/trainer/trainer.html',
        restrict: 'E',
        replace: true,
        scope: false,
        controller: function ($scope) {

          $scope.dynamic = 100;


          var getTrainInfo = function(){

            var out = {
              name: "Weight 1",
              date_started: "26th Sept, 2015",
              alpha: "0.01",
              speed: "26 batches/s",
              pid: "2335",
            }

            return out;
          };

          var getSavedWeights = function(){
            var out = [
              {
                id: 0,
                name: "24th Sept, 2015 4:23 PM Epoch 5"
              },
              {
                id: 1,
                name: "24th Sept, 2015 7:20 PM Epoch 8"
              }
              
            ]
              return out;
          };


         var getEvalInfo = function(){

            var out = {
              mean_error: "0.1432",
              accuracy: "57%",
              perplexicity: "154",
            }

            return out;
          };

          var getTestDatasets = function(){
            var out = [
              {
                id: 0,
                name: "Current Validation 20%"
              }              
            ]
              return out;
          };          


          $scope.trainInfo = getTrainInfo();
          $scope.savedWeights = getSavedWeights();

          $scope.evalInfo = getEvalInfo();
          $scope.datasets = getTestDatasets();

          $scope.currentTrainInfo = 0;


        }
    
    }
  });
