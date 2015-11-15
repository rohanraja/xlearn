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
        $scope.getRunJobs = function(x){
          $scope.check(x);
          listservice.getActiveJobs().then(function(resp){
            console.log(resp);
            $scope.activeJobs = resp;
          });
        };

        $scope.datasetId = $stateParams.datasetId ;
        console.log($scope.datasetId);
        $scope.modelId = $stateParams.modelId ;
        $scope.paramsId = $stateParams.paramsId ;
        $scope.collapseVar = $scope.activetab;
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
            $scope.collapseVar = $scope.activetab;

            for(var i=0; i<$scope.datasets.length; i++)
              if($scope.datasets[i].id == $scope.datasetId)
                $scope.activeDataset = $scope.datasets[i];
          });

          
        };

        $scope.$on('loadsidebar', function(event, mass){
          loadSideBar();
        });
        loadSideBar();

        $scope.$on('activetab', function(event, mass){
          $scope.activetab = mass;
        });

        
        $scope.onParamDelete = function(mid, pid){

          listservice.deleteParam(mid, pid).then(function(resp){
          
            loadSideBar();
          });

        };

        $scope.onDsetClick = function(x){
          
            $scope.collapseVar = 0;
            $scope.activeDataset = $scope.datasets[x];

        };



      }
    }
  }]);
