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
        controller: function ($scope, trainerservice, $timeout, listservice) {

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

              var d = trainerservice.startTraining($scope.modelId, $scope.paramsId, nepochs, $scope.currentWeight, $scope.valDatasetId);
              
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
          
          listservice.datasetList(0).then(function(resp){
            $scope.datasets = resp;
          });

          $scope.testDatasetId = 6;
          $scope.valDatasetId = 6;
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
