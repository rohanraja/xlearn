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

          var curEpoch = -1 ;

          $scope.trainer_running = false ;
          var stopping = false;

          $scope.onTrainDataRecieve = function(data){
            
            // $timeout(function() {
              
            if(stopping == false)
              $scope.trainer_running = true;
              $scope.trainInfo = JSON.parse(data.data);

              if(curEpoch != $scope.trainInfo.epoch){

               get_epochs();
              }

              curEpoch = $scope.trainInfo.epoch;
              
              $scope.epoch_percent = parseInt($scope.trainInfo["batch"]) / parseInt($scope.trainInfo["totbatches"]); 
              $scope.epoch_percent = parseInt($scope.epoch_percent * 100);

            // }, 0);

            $scope.$apply("trainInfo");
            $scope.$apply("epoch_percent");
          };

          trainerservice.attachHandler($scope.modelId, $scope.paramsId, $scope.onTrainDataRecieve);

          $scope.onTrainClick = function(){
             
            if ($scope.trainer_running == false){
              var nepochs = $scope.nepochs;

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
                name: "Nepal Tweet"
              },
              {
                id: 8,
                name: "Gurdaspur Tweets"
              }  ,
              {
                id: 3,
                name: "Brown 200"
              } ,
              {
                id: 4,
                name: "Brown 1000"
              }                      
            ]
              return out;
          };          


         $scope.currentWeight = 0;

         var get_epochs = function(){

          trainerservice.get_epoch_list($scope.modelId, $scope.paramsId).then(function(resp){

             if(resp.length > 0){
               $scope.currentWeight = resp[resp.length - 1].id;
               $scope.nepochs = resp[resp.length - 1].id + 1;
             }else{
               $scope.currentWeight = -1;
               $scope.nepochs = 10;
             }
             $scope.savedWeights = resp;
          });

         };
         get_epochs();


          // $scope.trainInfo = getTrainInfo();
          // $scope.savedWeights = getSavedWeights();

          // $scope.evalInfo = getEvalInfo();
          $scope.datasets = getTestDatasets();
          $scope.testDatasetId = 3;
          $scope.nsents = "0 10";

          $scope.currentTrainInfo = 0;

          $scope.onEvaluateClick = function(){
              
              $scope.evalPercent = 100;
              $scope.evalProgressText = "Calculating...";

              var d = trainerservice.startEvaluation($scope.modelId, $scope.paramsId, $scope.testDatasetId, $scope.currentWeight, $scope.nsents);
              
              d.then(function(resp){

                $scope.evalInfo = resp;
                $scope.evalPercent = parseInt(resp.accuracy);
                $scope.evalProgressText = resp.accuracy ;

              });

          };



        }
    
    }
  });
