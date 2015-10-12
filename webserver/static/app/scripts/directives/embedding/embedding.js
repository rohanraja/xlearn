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
        controller: function ($scope, listservice, trainerservice) {


          
          listservice.loadEmbeddings($scope.modelId).then(function(resp){
            $scope.embeddings = resp;
          });

          $scope.onPredictEmbedding = function(){
            trainerservice.predictWordEmbedding($scope.modelId, $scope.paramsId, $scope.word, $scope.currentWeight).then(function(resp){
              $scope.embed_results = resp;
            });
          };


        }
    
    }
  });
