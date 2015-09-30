'use strict';

/**
 * @ngdoc directive
 * @name izzyposWebApp.directive:adminPosHeader
 * @description
 * # adminPosHeader
 */

angular.module('sbAdminApp')
  .directive('sidebar',['$location',function() {
    return {
      templateUrl:'scripts/directives/sidebar/sidebar.html',
      restrict: 'E',
      replace: true,
      scope: {
      },
      controller:function($scope){
        $scope.selectedMenu = 'dashboard';
        $scope.collapseVar = 0;
        $scope.multiCollapseVar = 0;
        
        $scope.check = function(x){
          
          if(x==$scope.collapseVar)
            $scope.collapseVar = 0;
          else
            $scope.collapseVar = x;
        };
        
        $scope.multiCheck = function(y){
          
          if(y==$scope.multiCollapseVar)
            $scope.multiCollapseVar = 0;
          else
            $scope.multiCollapseVar = y;
        };

        $scope.datasets = [
          {
            name : 'Nepal Data English',
            models : [
              {
                name : 'RNN 2 layer'
              },
              {
                name : 'SVM radial'
              }
            ]
          },

          {
            name : 'Nepal Data Hindi',
            models : [
              {
                name : 'RNN 3 layer'
              },
              {
                name : 'SVM linear'
              }
           ]
          }

         ];

         $scope.activeDataset = $scope.datasets[0];

         $scope.onDsetClick = function(x){
          
            $scope.collapseVar = 0;
            $scope.activeDataset = $scope.datasets[x];

        };



      }
    }
  }]);
