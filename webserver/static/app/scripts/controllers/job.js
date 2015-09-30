angular.module('sbAdminApp')
  .controller('JobCtrl', function($scope,$position, $stateParams) {

    $scope.name = $stateParams.name ;


    $scope.jobInfo = {
      
      jobid: 1,
      dataset_id: 1,
      mapper_id: 2,
      embedding_id: 0,
      model_id: 0,

    }

    $scope.paramInfo = {
      
      jobid: 1,
      learn_embedding: 1,
      
      model: {
        input: "100",
        L1_output: "200",
        output:"100"
      },

      trainer: {
        optimizer: 'sgd',
        alpha: 0.1,
        decay: 0.001,
      }
    }


    $scope.$on('fork_model', function(event, mass) 
   {   
     alert("Clicked Model Fork");
   });


    var originalParams = angular.copy($scope.paramInfo) ;

    $scope.$watch('paramInfo', function(newVal, oldVal){

      if(JSON.stringify(newVal) != JSON.stringify(originalParams))
        $scope.$emit('fork_change', ['params', true]);
      else
        $scope.$emit('fork_change', ['params', false]);

    }, true);

    var originalJinfo = angular.copy($scope.jobInfo) ;

    $scope.$watch('jobInfo', function(newVal, oldVal){

      if(JSON.stringify(newVal) != JSON.stringify(originalJinfo))
        $scope.$emit('fork_change', ['model', true]);
      else
        $scope.$emit('fork_change', ['model', false]);

    }, true);

  }); 
