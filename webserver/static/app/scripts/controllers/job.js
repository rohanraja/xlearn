angular.module('sbAdminApp')
  .controller('JobCtrl', function($scope,$position, $stateParams, jobservice, $state) {

    // $scope.name = $stateParams.name ;

    $scope.activeTabs = [false, false, false, false, false];
    
    $scope.marktab = function(i){

        $scope.$root.$broadcast('activetab', i);
      // $stateParams.activetab = i;
      // $state.go('dashboard.job', $stateParams);

    };

    $scope.activeTabs[$stateParams.activetab] = true;

    $scope.datasetId = $stateParams.datasetId ;
    $scope.modelId = $stateParams.modelId ;
    $scope.paramsId = $stateParams.paramsId ;

    var originalJinfo;
    var originalParams;

    jobservice.getModelInfo($scope.modelId).then(function(resp){
       $scope.jobInfo = resp;
       originalJinfo = angular.copy($scope.jobInfo) ;

    });


    jobservice.getParamsInfo($scope.modelId, $scope.paramsId).then(function(resp){
       $scope.paramInfo = resp;
       originalParams = angular.copy($scope.paramInfo) ;

    });

    $scope.$on('fork_model', function(event, mass) 
    {   
      $scope.$root.$broadcast('loadsidebar');
    });

    $scope.$on('fork_params', function(event, mass) 
    {   
    
      jobservice.createParams($scope.modelId, $scope.paramInfo).then(function(resp){

        var newParamId = resp;
        console.log("Forked New Param with Id: ", newParamId);
        $scope.$root.$broadcast('loadsidebar');
        $state.go('dashboard.job', {datasetId: $scope.datasetId, modelId: $scope.modelId, paramsId: newParamId});
      });
    
    });





    $scope.$watch('paramInfo', function(newVal, oldVal){

      if(JSON.stringify(newVal) != JSON.stringify(originalParams))
        $scope.$emit('fork_change', ['params', true]);
      else
        $scope.$emit('fork_change', ['params', false]);

    }, true);


    $scope.$watch('jobInfo', function(newVal, oldVal){

      if(JSON.stringify(newVal) != JSON.stringify(originalJinfo))
        $scope.$emit('fork_change', ['model', true]);
      else
        $scope.$emit('fork_change', ['model', false]);

    }, true);

  }); 
