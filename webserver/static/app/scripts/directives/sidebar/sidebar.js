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
      controller:function($scope, $stateParams, listservice){

        // name = $stateParams.name ;

        $scope.selectedMenu = 'dashboard';
        $scope.collapseVar = 0;
        $scope.multiCollapseVar = 0;
        
        $scope.check = function(x){
          
          if(x==$scope.collapseVar)
            $scope.collapseVar = -1;
          else
            $scope.collapseVar = x;
        };
        
        $scope.multiCheck = function(y){
          
          if(y==$scope.multiCollapseVar)
            $scope.multiCollapseVar = 0;
          else
            $scope.multiCollapseVar = y;
        };


        var loadSideBar = function(){
          
          listservice.loadDatasets().then(function(resp){

            $scope.datasets = resp;

            $scope.datasetId = $stateParams.datasetId ;
            $scope.modelId = $stateParams.modelId ;
            $scope.paramsId = $stateParams.paramsId ;
            $scope.collapseVar = $scope.modelId;
            $scope.activeDataset = $scope.datasets[$scope.datasetId]; // Todo: Change
          });

          
        };

        $scope.$on('loadsidebar', function(event, mass){
          loadSideBar();
        });
        loadSideBar();

        $scope.$on('activetab', function(event, mass){
          $scope.activetab = mass;
        });

        

        $scope.onDsetClick = function(x){
          
            $scope.collapseVar = 0;
            $scope.activeDataset = $scope.datasets[x];

        };



      }
    }
  }]);
