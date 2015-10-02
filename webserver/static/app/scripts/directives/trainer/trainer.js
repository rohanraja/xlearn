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
        controller: function ($scope, trainerservice, $timeout) {

          $scope.epoch_percent = 0;

          $scope.trainer_running = false ;
          var stopping = false;

          $scope.onTrainDataRecieve = function(data){
            
            // $timeout(function() {
              
            if(stopping == false)
              $scope.trainer_running = true;
              $scope.trainInfo = JSON.parse(data.data);
              
              $scope.epoch_percent = parseInt($scope.trainInfo["batch"]) / parseInt($scope.trainInfo["totbatches"]); 
              $scope.epoch_percent = parseInt($scope.epoch_percent * 100);

            // }, 0);

            $scope.$apply("trainInfo");
            $scope.$apply("epoch_percent");
          };

          trainerservice.attachHandler($scope.modelId, $scope.paramsId, $scope.onTrainDataRecieve);

          $scope.onTrainClick = function(){
             
            if ($scope.trainer_running == false){
              var nepochs = 10;

              var d = trainerservice.startTraining($scope.modelId, $scope.paramsId, nepochs, $scope.currentWeight);
              
              d.then(function(resp){

                  trainerservice.attachHandler($scope.modelId, $scope.paramsId, $scope.onTrainDataRecieve);
                  $scope.trainer_running == true ;
                  stopping = false;

              });
            }
            else{

              var d = trainerservice.stopTraining($scope.modelId, $scope.paramsId);

              d.then(function(resp){
                
                stopping = true;

                $timeout(function() {
                  $scope.trainer_running = false ;
                }, 0);
                // $scope.$apply("trainer_running");
              });

            }

          };


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


         $scope.currentWeight = 0;
          trainerservice.get_epoch_list($scope.modelId, $scope.paramsId).then(function(resp){

             $scope.currentWeight = resp[resp.length - 1].id;
             $scope.savedWeights = resp;
          });


          // $scope.trainInfo = getTrainInfo();
          // $scope.savedWeights = getSavedWeights();

          $scope.evalInfo = getEvalInfo();
          $scope.datasets = getTestDatasets();

          $scope.currentTrainInfo = 0;


        }
    
    }
  });
