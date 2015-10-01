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
        controller: function ($scope) {

          var getWordResults = function(){
            
            var out = [
                    { 
                      word: "the",
                      score: "0.832"
                    },
                    { 
                      word: "eat",
                      score: "0.425"
                    },
            
                ];

            return out;

          };

          $scope.wordResults = getWordResults();
          var getTestResults = function(){
            
            var out = {

              "Probability": "0.45",
              "Perplexicity": "167"
              
            };

            return out;

          };

          $scope.testResults = getTestResults();


        }
    
    }
  });
